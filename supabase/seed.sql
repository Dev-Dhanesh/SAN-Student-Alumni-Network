-- ==============================================================================
-- College Career & Opportunity Network (SAN - Saveetha Alumni Network)
-- Seed Data: Authentic structure with EXPLICITLY LABELED FICTIONAL DEMO PROFILES
-- ==============================================================================

-- Note: In a live Supabase environment, users are created in auth.users first.
-- The UUIDs below are stable demo identifiers for local/staging testing.

-- 1. Demo Events (Hackathons, Symposiums, Competitions)
INSERT INTO public.events (id, title, organizer, category, description, mode, venue, event_date, registration_deadline, team_min_size, team_max_size, registration_link, is_demo)
VALUES
(
    'e1111111-1111-1111-1111-111111111111',
    'Saveetha InnoHack 2026 [College Hackathon]',
    'Saveetha Engineering College ACM Student Chapter',
    'hackathon',
    '36-hour flagship annual hackathon tackling real-world challenges across Healthcare, Sustainable Tech, and Autonomous Systems.',
    'offline',
    'Main Auditorium, Saveetha Campus, Chennai',
    NOW() + INTERVAL '25 days',
    NOW() + INTERVAL '10 days',
    2,
    4,
    'https://saveetha.ac.in/innohack',
    true
),
(
    'e2222222-2222-2222-2222-222222222222',
    'Smart India Hackathon (SIH) Internal Selection',
    'Center for Innovation & Incubation, Saveetha',
    'hackathon',
    'Internal campus qualifier round for Smart India Hackathon hardware and software problem statements.',
    'hybrid',
    'Innovation Lab 3, Department of CSE',
    NOW() + INTERVAL '40 days',
    NOW() + INTERVAL '15 days',
    3,
    6,
    'https://sih.gov.in',
    true
),
(
    'e3333333-3333-3333-3333-333333333333',
    'National Symposium on Cloud Computing & Distributed AI',
    'Department of Information Technology, Saveetha',
    'symposium',
    'Paper presentations and competitive speed-coding challenges on scalable distributed microservices.',
    'offline',
    'Seminar Hall B, Saveetha Campus',
    NOW() + INTERVAL '30 days',
    NOW() + INTERVAL '18 days',
    1,
    2,
    'https://saveetha.ac.in/symposium-ccda',
    true
)
ON CONFLICT (id) DO NOTHING;

-- 2. Demo Opportunities (Jobs & Internships explicitly labeled)
INSERT INTO public.opportunities (id, title, company, type, location_type, location, stipend_salary, description, skills_required, eligibility, application_link, deadline, is_verified, is_approved, is_demo)
VALUES
(
    'o1111111-1111-1111-1111-111111111111',
    'Software Development Engineer Intern [Demo Listing]',
    'Amazon Web Services (AWS)',
    'internship',
    'hybrid',
    'Chennai / Bangalore',
    '₹80,000 / month',
    '6-month winter/summer internship working on distributed cloud services. Alumni referral available for qualified 3rd & 4th year candidates.',
    ARRAY['Java', 'C++', 'Data Structures', 'Algorithms', 'Distributed Systems'],
    '3rd or 4th year B.E/B.Tech (CSE, IT, ECE) with CGPA >= 7.5',
    'https://amazon.jobs',
    NOW() + INTERVAL '20 days',
    true,
    true,
    true
),
(
    'o2222222-2222-2222-2222-222222222222',
    'Product Engineering Intern [Demo Listing]',
    'Zoho Corporation',
    'internship',
    'on-site',
    'Estancia IT Park, Guduvanchery, Chennai',
    '₹25,000 / month (with PPO)',
    'Hands-on product development for SaaS suite applications. Heavy focus on raw problem solving, pointers, and memory efficiency.',
    ARRAY['C', 'Java', 'Data Structures', 'OOP', 'SQL'],
    '2nd, 3rd, and 4th year students across all branches',
    'https://zoho.com/careers',
    NOW() + INTERVAL '14 days',
    true,
    true,
    true
),
(
    'o3333333-3333-3333-3333-333333333333',
    'Junior Full-Stack Developer [Demo Listing]',
    'Freshworks Inc.',
    'job',
    'hybrid',
    'Chennai',
    '₹8.5 - 12 LPA',
    'Building modern customer engagement interfaces and scalable backend APIs using Ruby on Rails and React.',
    ARRAY['JavaScript', 'React', 'Ruby/Python', 'PostgreSQL', 'REST APIs'],
    'Graduating 2026 or 2025 alumni',
    'https://freshworks.com/careers',
    NOW() + INTERVAL '30 days',
    true,
    true,
    true
)
ON CONFLICT (id) DO NOTHING;
