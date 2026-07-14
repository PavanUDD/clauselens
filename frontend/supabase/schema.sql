-- Run this once in the Supabase SQL editor for your project.
-- Stores analysis summaries only — never the underlying contract text.

create table if not exists public.analyses (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  filename text not null,
  contract_type text not null,
  grade text not null,
  high_flags integer not null default 0,
  medium_flags integer not null default 0,
  low_flags integer not null default 0,
  analyzed_at timestamptz not null default now()
);

create index if not exists analyses_user_id_idx on public.analyses (user_id);

alter table public.analyses enable row level security;

create policy "Users can view their own analyses"
  on public.analyses for select
  using (auth.uid() = user_id);

create policy "Users can insert their own analyses"
  on public.analyses for insert
  with check (auth.uid() = user_id);
