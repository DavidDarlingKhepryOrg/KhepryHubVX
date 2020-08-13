CREATE INDEX IF NOT EXISTS ix_nc_voter_history_county_id ON nc_voter_history (county_id);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_election_lbl ON nc_voter_history (election_lbl);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_ncid ON nc_voter_history (ncid);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_pct_label ON nc_voter_history (pct_label);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_voted_county_id ON nc_voter_history (voted_county_id);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_vtd_label ON nc_voter_history (vtd_label);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_voted_party_cd ON nc_voter_history (voted_party_cd);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_voter_reg_num ON nc_voter_history (voter_reg_num);
CREATE INDEX IF NOT EXISTS ix_nc_voter_history_voting_method ON nc_voter_history (voting_method);
