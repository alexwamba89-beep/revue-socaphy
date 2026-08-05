import os
def w(name, content):
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)

sql = r'''-- ============================================================================
-- SOCAphy - Espace admin (lecture et gestion des soumissions)
-- A executer dans Supabase : SQL Editor > New query > coller > Run
-- ============================================================================

-- 1) Colonne "traite" pour marquer une demande / candidature comme traitee
alter table public.candidatures add column if not exists traite boolean not null default false;
alter table public.demandes     add column if not exists traite boolean not null default false;

-- 2) Politiques RLS : les utilisateurs AUTHENTIFIES (les admins connectes)
--    peuvent LIRE, MODIFIER et SUPPRIMER. Le public "anon" garde uniquement
--    le droit d'inserer (defini precedemment). Aucune lecture publique.
create policy "admin lecture candidatures"     on public.candidatures for select to authenticated using (true);
create policy "admin maj candidatures"         on public.candidatures for update to authenticated using (true) with check (true);
create policy "admin suppression candidatures" on public.candidatures for delete to authenticated using (true);

create policy "admin lecture demandes"     on public.demandes for select to authenticated using (true);
create policy "admin maj demandes"         on public.demandes for update to authenticated using (true) with check (true);
create policy "admin suppression demandes" on public.demandes for delete to authenticated using (true);

-- ============================================================================
-- IMPORTANT - Securite :
-- Apres avoir lance ce script, va dans Supabase > Authentication > Sign In / Providers
-- (ou Settings) et DESACTIVE "Allow new users to sign up".
-- Sinon, n'importe qui pourrait creer un compte et lire tes donnees.
-- Tu creeras toi-meme les comptes admin dans Authentication > Users > Add user.
-- ============================================================================
'''
w("socaphy_admin.sql", sql)
print("SQL admin ecrit")
