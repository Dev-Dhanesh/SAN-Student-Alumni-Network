-- ==============================================================================
-- College Career & Opportunity Network (SAN - Saveetha Alumni Network)
-- Migration 001: Schema Definition & pgvector Setup
-- ==============================================================================

-- Enable pgvector extension for semantic similarity queries
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Student Profiles (1-to-1 with auth.users)
CREATE TABLE IF NOT EXISTS public.student_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    current_year INT NOT NULL CHECK (current_year BETWEEN 1 AND 4),
    expected_graduation_year INT NOT NULL,
    skills TEXT[] DEFAULT '{}',
    interests TEXT[] DEFAULT '{}',
    career_goals TEXT,
    bio TEXT,
    github_url TEXT,
    linkedin_url TEXT,
    portfolio_url TEXT,
    is_looking_for_team BOOLEAN DEFAULT true,
    preferred_roles TEXT[] DEFAULT '{}',
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Alumni Profiles (1-to-1 with auth.users)
CREATE TABLE IF NOT EXISTS public.alumni_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    department TEXT NOT NULL,
    graduation_year INT NOT NULL,
    current_company TEXT NOT NULL,
    current_role TEXT NOT NULL,
    industry TEXT,
    location TEXT,
    skills TEXT[] DEFAULT '{}',
    bio TEXT,
    linkedin_url TEXT,
    is_available_for_mentorship BOOLEAN DEFAULT false,
    mentorship_categories TEXT[] DEFAULT '{}',
    years_of_experience INT DEFAULT 1,
    is_verified BOOLEAN DEFAULT false,
    is_demo BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Opportunities (Jobs and Internships exclusively)
CREATE TABLE IF NOT EXISTS public.opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('job', 'internship')),
    location_type TEXT NOT NULL CHECK (location_type IN ('remote', 'on-site', 'hybrid')),
    location TEXT,
    stipend_salary TEXT,
    description TEXT NOT NULL,
    skills_required TEXT[] DEFAULT '{}',
    eligibility TEXT,
    application_link TEXT NOT NULL,
    deadline TIMESTAMPTZ,
    posted_by UUID REFERENCES public.alumni_profiles(user_id) ON DELETE SET NULL,
    is_verified BOOLEAN DEFAULT false,
    is_approved BOOLEAN DEFAULT true,
    is_demo BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Events (Hackathons, Coding Contests, Workshops, Symposiums, Conferences)
CREATE TABLE IF NOT EXISTS public.events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    organizer TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('hackathon', 'coding_contest', 'workshop', 'symposium', 'paper_presentation', 'other')),
    description TEXT NOT NULL,
    mode TEXT NOT NULL CHECK (mode IN ('online', 'offline', 'hybrid')),
    venue TEXT,
    event_date TIMESTAMPTZ,
    registration_deadline TIMESTAMPTZ,
    team_min_size INT DEFAULT 1,
    team_max_size INT DEFAULT 4,
    registration_link TEXT,
    is_demo BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Event Registrations (Student participation in events)
CREATE TABLE IF NOT EXISTS public.event_registrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID NOT NULL REFERENCES public.events(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.student_profiles(user_id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'registered' CHECK (status IN ('registered', 'attended', 'cancelled')),
    registered_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(event_id, student_id)
);

-- 6. Teams (Teams created by students for events)
CREATE TABLE IF NOT EXISTS public.teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES public.events(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    creator_id UUID NOT NULL REFERENCES public.student_profiles(user_id) ON DELETE CASCADE,
    target_team_size INT NOT NULL CHECK (target_team_size >= 2),
    needed_roles TEXT[] DEFAULT '{}',
    needed_skills TEXT[] DEFAULT '{}',
    deadline TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'full', 'closed')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Team Members (Dynamic membership without redundant counter)
CREATE TABLE IF NOT EXISTS public.team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES public.teams(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.student_profiles(user_id) ON DELETE CASCADE,
    role_in_team TEXT NOT NULL,
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, student_id)
);

-- 8. Team Join Requests
CREATE TABLE IF NOT EXISTS public.team_join_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES public.teams(id) ON DELETE CASCADE,
    applicant_id UUID NOT NULL REFERENCES public.student_profiles(user_id) ON DELETE CASCADE,
    message TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(team_id, applicant_id)
);

-- 9. Career Journeys (Chronological multi-stage pathways shared by alumni)
CREATE TABLE IF NOT EXISTS public.career_journeys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alumni_id UUID NOT NULL REFERENCES public.alumni_profiles(user_id) ON DELETE CASCADE,
    stages JSONB NOT NULL DEFAULT '[]'::jsonb,
    mistakes_made TEXT,
    lessons_learned TEXT,
    advice_for_juniors TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Interview Experiences (Searchable database with interview rounds and prep topics)
CREATE TABLE IF NOT EXISTS public.interview_experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alumni_id UUID NOT NULL REFERENCES public.alumni_profiles(user_id) ON DELETE CASCADE,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    year INT NOT NULL,
    department TEXT NOT NULL,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    outcome TEXT NOT NULL CHECK (outcome IN ('offered', 'rejected')),
    rounds JSONB NOT NULL DEFAULT '[]'::jsonb,
    topics_covered TEXT[] DEFAULT '{}',
    preparation_resources TEXT,
    advice TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Mentorship Requests
CREATE TABLE IF NOT EXISTS public.mentorship_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.student_profiles(user_id) ON DELETE CASCADE,
    alumni_id UUID NOT NULL REFERENCES public.alumni_profiles(user_id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined', 'completed')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. Saved Opportunities (Bookmarking)
CREATE TABLE IF NOT EXISTS public.saved_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    opportunity_id UUID NOT NULL REFERENCES public.opportunities(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, opportunity_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_student_skills ON public.student_profiles USING GIN (skills);
CREATE INDEX IF NOT EXISTS idx_alumni_company ON public.alumni_profiles (current_company);
CREATE INDEX IF NOT EXISTS idx_opp_skills ON public.opportunities USING GIN (skills_required);
CREATE INDEX IF NOT EXISTS idx_interview_comp_role ON public.interview_experiences (company, role);
CREATE INDEX IF NOT EXISTS idx_team_status ON public.teams (status);
