create index idx_voter_master_last_name_btree on voter_master using BTREE((resource->>'last_Name'));
create index idx_voter_master_first_name_btree on voter_master using BTREE((resource->>'first_Name'));
create index idx_voter_master_regist_dt_btree on voter_master using BTREE((resource->>'regist_dt'));
