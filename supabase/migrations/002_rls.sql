-- ==============================================================================
-- College Career & Opportunity Network (SAN - Saveetha Alumni Network)
-- Migration 002: Row Level Security (RLS) Policies
-- ==============================================================================

-- Enable RLS on all tables
ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alumni_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.event_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.teams ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.team_join_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.career_journeys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interview_experiences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mentorship_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.saved_opportunities ENABLE ROW LEVEL SECURITY;

-- 1. Student Profiles
CREATE POLICY "Public read student profiles" ON public.student_profiles
    FOR SELECT USING (true);
CREATE POLICY "Students can update own profile" ON public.student_profiles
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Students can insert own profile" ON public.student_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 2. Alumni Profiles
CREATE POLICY "Public read alumni profiles" ON public.alumni_profiles
    FOR SELECT USING (true);
CREATE POLICY "Alumni can update own profile" ON public.alumni_profiles
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Alumni can insert own profile" ON public.alumni_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 3. Opportunities
CREATE POLICY "Public read approved opportunities" ON public.opportunities
    FOR SELECT USING (is_approved = true);
CREATE POLICY "Alumni can insert opportunities" ON public.opportunities
    FOR INSERT WITH CHECK (auth.uid() = posted_by);
CREATE POLICY "Alumni can update own opportunities" ON public.opportunities
    FOR UPDATE USING (auth.uid() = posted_by);

-- 4. Events
CREATE POLICY "Public read events" ON public.events
    FOR SELECT USING (true);

-- 5. Event Registrations
CREATE POLICY "Users can read own registrations" ON public.event_registrations
    FOR SELECT USING (auth.uid() = student_id);
CREATE POLICY "Students can register for events" ON public.event_registrations
    FOR INSERT WITH CHECK (auth.uid() = student_id);
CREATE POLICY "Students can cancel registration" ON public.event_registrations
    FOR DELETE USING (auth.uid() = student_id);

-- 6. Teams
CREATE POLICY "Public read teams" ON public.teams
    FOR SELECT USING (true);
CREATE POLICY "Students can create teams" ON public.teams
    FOR INSERT WITH CHECK (auth.uid() = creator_id);
CREATE POLICY "Creators can update team" ON public.teams
    FOR UPDATE USING (auth.uid() = creator_id);

-- 7. Team Members
CREATE POLICY "Public read team members" ON public.team_members
    FOR SELECT USING (true);
CREATE POLICY "Creators or members can insert" ON public.team_members
    FOR INSERT WITH CHECK (true);

-- 8. Team Join Requests
CREATE POLICY "Team creator or applicant can read requests" ON public.team_join_requests
    FOR SELECT USING (
        auth.uid() = applicant_id OR 
        EXISTS (SELECT 1 FROM public.teams WHERE id = team_id AND creator_id = auth.uid())
    );
CREATE POLICY "Students can submit join request" ON public.team_join_requests
    FOR INSERT WITH CHECK (auth.uid() = applicant_id);
CREATE POLICY "Team creator can update request status" ON public.team_join_requests
    FOR UPDATE USING (
        EXISTS (SELECT 1 FROM public.teams WHERE id = team_id AND creator_id = auth.uid())
    );

-- 9. Career Journeys
CREATE POLICY "Public read career journeys" ON public.career_journeys
    FOR SELECT USING (true);
CREATE POLICY "Alumni can create own journey" ON public.career_journeys
    FOR INSERT WITH CHECK (auth.uid() = alumni_id);
CREATE POLICY "Alumni can update own journey" ON public.career_journeys
    FOR UPDATE USING (auth.uid() = alumni_id);

-- 10. Interview Experiences
CREATE POLICY "Public read interview experiences" ON public.interview_experiences
    FOR SELECT USING (true);
CREATE POLICY "Alumni can contribute interview experience" ON public.interview_experiences
    FOR INSERT WITH CHECK (auth.uid() = alumni_id);

-- 11. Mentorship Requests
CREATE POLICY "Student or alumni can view request" ON public.mentorship_requests
    FOR SELECT USING (auth.uid() = student_id OR auth.uid() = alumni_id);
CREATE POLICY "Student can create mentorship request" ON public.mentorship_requests
    FOR INSERT WITH CHECK (auth.uid() = student_id);
CREATE POLICY "Alumni can update request status" ON public.mentorship_requests
    FOR UPDATE USING (auth.uid() = alumni_id);

-- 12. Saved Opportunities
CREATE POLICY "Users can manage own saved opportunities" ON public.saved_opportunities
    FOR ALL USING (auth.uid() = user_id);
