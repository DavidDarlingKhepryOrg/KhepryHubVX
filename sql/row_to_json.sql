truncate table voter_master;

with cte_voters_tweaked as
(
	select
		county_id,
		trim(county_desc) as county_desc,
		cast(voter_reg_num as integer) as voter_reg_num,
		trim(status_cd) as status_cd,
		trim(voter_status_desc) as voter_status_desc,
		trim(reason_cd) as reason_cd,
		trim(voter_status_reason_desc) as voter_status_reason_desc,
		trim(absent_ind) as absent_ind,
		trim(name_prefx_cd) as name_prfx_cd,
		trim(last_name) as last_name,
		trim(first_name) as first_name,
		trim(middle_name) as middle_name,
		trim(name_suffix_lbl) as name_suffix_lbl, 
		trim(res_street_address) as res_street_address,
		trim(res_city_desc) as res_city_desc,
		trim(state_cd) as state_cd,
		trim(zip_code) as zip_code,
		trim(mail_addr1) as mail_addr1,
		trim(mail_addr2) as mail_addr2,
		trim(mail_addr3) as mail_addr3,
		trim(mail_addr4) as mail_addr4,
		trim(mail_city) as mail_city,
		trim(mail_state) as mail_state,
		trim(mail_zipcode) as mail_zipcode,
		trim(full_phone_number) as full_phone_number,
		trim(race_code) as race_code,
		trim(ethnic_code) as ethnic_code,
		trim(party_cd) as party_cd,
		trim(gender_code) as gender_code,
		birth_age,
		trim(birth_state) as birth_state,
		trim(drivers_lic) as drivers_lic,
		to_char(registr_dt, 'YYYY-MM-DD') as regist_dt,
		trim(precinct_abbrv) as precinct_abbrv,
		trim(precinct_desc) as precinct_desc,
		trim(municipality_abbrv) as municipality_abbrv,
		trim(municipality_desc) as municipality_desc,
		trim(ward_abbrv) as ward_abbrv,
		trim(ward_desc) as ward_desc,
		trim(cong_dist_abbrv) as cong_dist_abbrv,
		trim(super_court_abbrv) as super_court_abbrv,
		trim(judic_dist_abbrv) as judic_dist_abbrv,
		trim(nc_senate_abbrv) as nc_senate_abbrv,
		trim(nc_house_abbrv) as nc_house_abbrv,
		trim(county_commiss_abbrv) as county_commiss_abbrv,
		trim(county_commiss_desc) as county_commiss_desc,
		trim(township_abbrv) as township_abbrv,
		trim(township_desc) as township_desc,
		trim(school_dist_abbrv) as school_dist_abbrv,
		trim(school_dist_desc) as school_dist_desc,
		trim(fire_dist_abbrv) as fire_dist_abbrv,
		trim(fire_dist_desc) as fire_dist_desc,
		trim(water_dist_abbrv) as water_dist_abbrv,
		trim(water_dist_desc) as water_dist_desc,
		trim(sewer_dist_abbrv) as sewer_dist_abbrv,
		trim(sewer_dist_desc) as sewer_dist_desc,
		trim(sanit_dist_abbrv) as sanit_dist_abbrv,
		trim(sanit_dist_desc) as sanit_dist_desc,
		trim(rescue_dist_abbrv) as rescue_dist_abbrv,
		trim(rescue_dist_desc) as rescue_dist_desc,
		trim(munic_dist_abbrv) as munic_dist_abbrv,
		trim(munic_dist_desc) as munic_dist_desc,
		trim(dist_1_abbrv) as dist_1_abbrv,
		trim(dist_1_desc) as dist_1_desc,
		trim(dist_2_abbrv) as dist_2_abbrv,
		trim(dist_2_desc) as dist_2_desc,
		trim(confidential_ind) as confidential_ind,
		trim(birth_year) as birth_year,
		trim(ncid) as ncid,
		trim(vtd_abbrv) as vtd_abbrv,
		trim(vtd_desc) as vtd_desc
	FROM public.nc_voter_master
),
cte_jsonb_rows as
(
	select
		to_jsonb(cte_voters_tweaked) as resource
	from
		cte_voters_tweaked
)
insert into voter_master (id, txid, ts, resource_type, status, resource, hex_digest)
select
	uuid_generate_v4() as id,
	0 as txid,
	NOW() as ts,
	'voter_master' as resource_type,
	'created' as status,
	resource,
	encode(sha256(resource::text::bytea), 'hex') as hex_digest
from
	cte_jsonb_rows
;

