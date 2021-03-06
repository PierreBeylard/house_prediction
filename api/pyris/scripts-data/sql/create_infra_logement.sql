-- logement infra communale (IRIS)
DROP TABLE IF EXISTS insee.logement_{census};

CREATE TABLE IF NOT EXISTS insee.logement_{census} (
  iris varchar(9) PRIMARY KEY,
  reg varchar(2),
  dep varchar(3),
  uu2010 varchar(5),
  com varchar(5),
  libcom varchar(50),
  triris varchar(6),
  grd_quart varchar(7),
  libiris varchar(80),
  typ_iris varchar(1),
  modif_iris varchar(10),
  lab_iris varchar(1),
  P_LOG float,
 P_RP float,
 P_RSECOCC float,
 P_LOGVAC float,
 P_MAISON float,
 P_APPART float,
 P_RP_1P float,
 P_RP_2P float,
 P_RP_3P float,
 P_RP_4P float,
 P_RP_5PP float,
 P_NBPI_RP float,
 P_RPMAISON float,
 P_NBPI_RPMAISON float,
 P_RPAPPART float,
 P_NBPI_RPAPPART float,
 P_RP_M30M2 float,
 P_RP_3040M2 float,
 P_RP_4060M2 float,
 P_RP_6080M2 float,
 P_RP_80100M2 float,
 P_RP_100120M2 float,
 P_RP_120M2P float,
 P_RP_ACHTOT float,
 P_RP_ACH19 float,
 P_RP_ACH45 float,
 P_RP_ACH70 float,
 P_RP_ACH90 float,
 P_RP_ACH05 float,
 P_RP_ACH14 float,
 P_RPMAISON_ACHTOT float,
 P_RPMAISON_ACH19 float,
 P_RPMAISON_ACH45 float,
 P_RPMAISON_ACH70 float,
 P_RPMAISON_ACH90 float,
 P_RPMAISON_ACH05 float,
 P_RPMAISON_ACH14 float,
 P_RPAPPART_ACHTOT float,
 P_RPAPPART_ACH19 float,
 P_RPAPPART_ACH45 float,
 P_RPAPPART_ACH70 float,
 P_RPAPPART_ACH90 float,
 P_RPAPPART_ACH05 float,
 P_RPAPPART_ACH14 float,
 P_MEN float,
 P_MEN_ANEM0002 float,
 P_MEN_ANEM0204 float,
 P_MEN_ANEM0509 float,
 P_MEN_ANEM10P float,
 P_PMEN float,
 P_PMEN_ANEM0002 float,
 P_PMEN_ANEM0204 float,
 P_PMEN_ANEM0509 float,
 P_PMEN_ANEM10P float,
 P_NBPI_RP_ANEM0002 float,
 P_NBPI_RP_ANEM0204 float,
 P_NBPI_RP_ANEM0509 float,
 P_NBPI_RP_ANEM10P float,
 P_RP_PROP float,
 P_RP_LOC float,
 P_RP_LOCHLMV float,
 P_RP_GRAT float,
 P_NPER_RP float,
 P_NPER_RP_PROP float,
 P_NPER_RP_LOC float,
 P_NPER_RP_LOCHLMV float,
 P_NPER_RP_GRAT float,
 P_ANEM_RP float,
 P_ANEM_RP_PROP float,
 P_ANEM_RP_LOC float,
 P_ANEM_RP_LOCHLMV float,
 P_ANEM_RP_GRAT float,
 P_RP_SDB float,
 P_RP_CCCOLL float,
 P_RP_CCIND float,
 P_RP_CINDELEC float,
 P_RP_ELEC float,
 P_RP_EAUCH float,
 P_RP_BDWC float,
 P_RP_CHOS float,
 P_RP_CLIM float,
 P_RP_TTEGOU float,
 P_RP_GARL float,
 P_RP_VOIT1P float,
 P_RP_VOIT1 float,
 P_RP_VOIT2P float,
 P_RP_HABFOR float,
 P_RP_CASE float,
 P_RP_MIBOIS float,
 P_RP_MIDUR float,
 C_RP_HSTU1P float,
 C_RP_HSTU1P_SUROCC float
);


create index logement_{census}_dep_idx ON insee.logement_{census} USING btree (dep);
create index logement_{census}_com_idx ON insee.logement_{census} USING btree (com);
create index logement_{census}_libcom_idx ON insee.logement_{census} USING btree (libcom);


COMMENT ON TABLE insee.logement_{census} IS 'logement ?? l''IRIS (source Insee), census {census}';

COMMENT ON COLUMN insee.logement_{census}.iris IS 'IRIS';
COMMENT ON COLUMN insee.logement_{census}.reg IS 'R??gion (nouvelle)';
COMMENT ON COLUMN insee.logement_{census}.dep IS 'D??partement';
COMMENT ON COLUMN insee.logement_{census}.uu2010 IS 'Unit?? urbaine';
COMMENT ON COLUMN insee.logement_{census}.com IS 'Commune ou ARM';
COMMENT ON COLUMN insee.logement_{census}.libcom IS 'Libell?? commune ou ARM';
COMMENT ON COLUMN insee.logement_{census}.triris IS 'TRIRIS';
COMMENT ON COLUMN insee.logement_{census}.grd_quart IS 'Grand quartier';
COMMENT ON COLUMN insee.logement_{census}.libiris IS 'Libell?? de l''IRIS';
COMMENT ON COLUMN insee.logement_{census}.typ_iris IS 'Type d''IRIS';
COMMENT ON COLUMN insee.logement_{census}.modif_iris IS 'Modification de l''IRIS';
COMMENT ON COLUMN insee.logement_{census}.lab_iris IS 'Label de l''IRIS';

COMMENT ON COLUMN insee.logement_{census}.p_log IS 'Logements (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp IS 'R??sidences principales (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rsecocc IS 'R??s secondaires et logts occasionnels (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_logvac IS 'Logements vacants (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_maison IS 'Maisons (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_appart IS 'Appartements (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_1p IS 'R??s princ 1 pi??ce (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_2p IS 'R??s princ 2 pi??ces (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_3p IS 'R??s princ 3 pi??ces (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_4p IS 'R??s princ 4 pi??ces (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_5pp IS 'R??s princ 5 pi??ces ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rp IS 'Pi??ces r??s princ (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison IS 'R??s princ type maison (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rpmaison IS 'Pi??ces r??s princ type maison (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart IS 'R??s princ type appartement (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rpappart IS 'Pi??ces r??s princ type appartement (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_m30m2 IS 'R??s princ de moins de 30 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_3040m2 IS 'R??s princ de 30 ?? moins de 40 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_4060m2 IS 'R??s princ de 40 ?? moins de 60 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_6080m2 IS 'R??s princ de 60 ?? moins de 80 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_80100m2 IS 'R??s princ de 80 ?? moins de 100 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_100120m2 IS 'R??s princ de 100 ?? moins de 120 m2 (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_120m2p IS 'R??s princ de 120 m2 ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_achtot IS 'R??s princ avt 2011 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ach19 IS 'R??s princ avt 1919 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ach45 IS 'R??s princ 1919 ?? 1945 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ach70 IS 'R??s princ 1946 ?? 1970 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ach90 IS 'R??s princ 1971 ?? 1990 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ach05 IS 'R??s princ 1991 ?? 2005 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.P_RP_ACH14 IS 'R??s princ 2006 ?? 2014 en 2017 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_achtot IS 'R??s princ Type maison avt 2011 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_ach19 IS 'R??s princ Type maison avt 1919 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_ach45 IS 'R??s princ Type maison 1919 ?? 1945 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_ach70 IS 'R??s princ Type maison 1946 ?? 1970 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_ach90 IS 'R??s princ Type maison 1971 ?? 1990 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpmaison_ach05 IS 'R??s princ Type maison 1991 ?? 2005 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.P_RPMAISON_ACH14 IS 'R??s princ Type maison 2006 ?? 2014 en 2017 (princ)  ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_achtot IS 'R??s princ Type appart avt 2011 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_ach19 IS 'R??s princ Type appart avt 1919 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_ach45 IS 'R??s princ Type appart 1919 ?? 1945 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_ach70 IS 'R??s princ Type appart 1946 ?? 1970 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_ach90 IS 'R??s princ Type appart 1971 ?? 1990 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.p_rpappart_ach05 IS 'R??s princ Type appart 1991 ?? 2005 (princ) ';
COMMENT ON COLUMN insee.logement_{census}.P_RPAPPART_ACH14 IS 'R??s princ Type appart 2006 ?? 2014 en 2017 (princ)  ';
COMMENT ON COLUMN insee.logement_{census}.p_men IS 'M??nages (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_men_anem0002 IS 'M??nages emm??nag??s moins 2 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_men_anem0204 IS 'M??nages emm??nag??s entre 2-4 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_men_anem0509 IS 'M??nages emm??nag??s entre 5-9 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_men_anem10p IS 'M??nages emm??nag??s depuis 10 ans ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_pmen IS 'Pop m??nages (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_pmen_anem0002 IS 'Pop m??n emm??nag??s moins 2 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_pmen_anem0204 IS 'Pop m??n emm??nag??s entre 2-4 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_pmen_anem0509 IS 'Pop m??n emm??nag??s entre 5-9 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_pmen_anem10p IS 'Pop m??n emm??nag??s depuis 10 ans ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rp_anem0002 IS 'Pi??ces R??s princ M??n. emm??nag??s moins 2 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rp_anem0204 IS 'Pi??ces R??s princ M??n. emm??nag??s entre 2-4 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rp_anem0509 IS 'Pi??ces R??s princ M??n. emm??nag??s entre 5-9 ans (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nbpi_rp_anem10p IS 'Pi??ces R??s princ M??n. emm??nag??s depuis 10 ans ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_prop IS 'R??s princ occup??es Propri??taires (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_loc IS 'R??s princ occup??es Locataires (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_lochlmv IS 'R??s princ HLM lou??e vide (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_grat IS 'R??s princ log?? gratuit (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nper_rp IS 'Personnes R??s princ (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nper_rp_prop IS 'Pers R??s princ occup??es Propri??taires (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nper_rp_loc IS 'Pers R??s princ occup??es Locataires (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nper_rp_lochlmv IS 'Pers R??s princ HLM lou??es vides (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_nper_rp_grat IS 'Pers R??s princ occup??es gratuit (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_anem_rp IS 'Anc tot Emm??ngt R??s princ (ann??es) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_anem_rp_prop IS 'Anc tot Emm??ngt R??s princ occ par Propri??taires (ann??es) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_anem_rp_loc IS 'Anc tot Emm??ngt R??s princ occ par Locataires (ann??es) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_anem_rp_lochlmv IS 'Anc tot Emm??ngt R??s princ HLM lou??es vides (ann??es) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_anem_rp_grat IS 'Anc tot Emm??ngt R??s princ occ gratuit (ann??es) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_sdb IS 'R??s princ SDB baignoire douche (MET) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_cccoll IS 'R??s princ Chauffage Central Collectif (MET) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ccind IS 'R??s princ Chauffage Central Individuel (MET) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_cindelec IS 'R??s princ Chauffage Individuel Electrique (MET) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_elec IS 'R??s princ avec ??lectricit?? (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_eauch IS 'R??s princ avec eau chaude (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_bdwc IS 'R??s princ avec Bain/Douche WC (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_chos IS 'R??s princ avec chauffe-eau solaire (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_clim IS 'R??s princ avec pi??ce climatis??e (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_ttegou IS 'R??s princ avec tout ?? l''??gout (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_garl IS 'M??nages au moins un parking (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_voit1p IS 'M??nages au moins une voiture (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_voit1 IS 'M??nages une voiture (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_voit2p IS 'M??nages deux voitures ou plus (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_habfor IS 'Habitations de fortune (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_case IS 'Cases traditionnelles (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_mibois IS 'Maisons ou Immeubles en bois (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.p_rp_midur IS 'Maisons ou Immeubles en dur (DOM) (princ)';
COMMENT ON COLUMN insee.logement_{census}.C_RP_HSTU1P IS 'R??s princ (hors studio de 1 personne) en 2017 (compl)';
COMMENT ON COLUMN insee.logement_{census}.C_RP_HSTU1P_SUROCC IS 'R??s princ (hors studio de 1 personne) en suroccupation en 2017 (compl)';

\copy insee.logement_{census} FROM '{fpath}' DELIMITER '{sep}' CSV HEADER;
