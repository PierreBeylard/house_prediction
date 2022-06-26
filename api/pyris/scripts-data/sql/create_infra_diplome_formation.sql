-- diplomes formation infra communale (IRIS)
DROP TABLE IF EXISTS insee.diplome_formation_{census};

CREATE TABLE IF NOT EXISTS insee.diplome_formation_{census} (
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
 P_POP0205 float,
 P_POP0610 float,
 P_POP1114 float,
 P_POP1517 float,
 P_POP1824 float,
 P_POP2529 float,
 P_POP30P float,
 P_SCOL0205 float,
 P_SCOL0610 float,
 P_SCOL1114 float,
 P_SCOL1517 float,
 P_SCOL1824 float,
 P_SCOL2529 float,
 P_SCOL30P float,
 P_NSCOL15P float,
 P_NSCOL15P_DIPLMIN float,
 P_NSCOL15P_BEPC float,
 P_NSCOL15P_CAPBEP float,
 P_NSCOL15P_BAC float,
 P_NSCOL15P_SUP2 float,
 P_NSCOL15P_SUP34 float,
 P_NSCOL15P_SUP5 float,
 P_HNSCOL15P float,
 P_HNSCOL15P_DIPLMIN float,
 P_HNSCOL15P_BEPC float,
 P_HNSCOL15P_CAPBEP float,
 P_HNSCOL15P_BAC float,
 P_HNSCOL15P_SUP2 float,
 P_HNSCOL15P_SUP34 float,
 P_HNSCOL15P_SUP5 float,
 P_FNSCOL15P float,
 P_FNSCOL15P_DIPLMIN float,
 P_FNSCOL15P_BEPC float,
 P_FNSCOL15P_CAPBEP float,
 P_FNSCOL15P_BAC float,
 P_FNSCOL15P_SUP2 float,
 P_FNSCOL15P_SUP34 float,
 P_FNSCOL15P_SUP5 float
);


create index diplome_formation_{census}_dep_idx ON insee.diplome_formation_{census} USING btree (dep);
create index diplome_formation_{census}_com_idx ON insee.diplome_formation_{census} USING btree (com);
create index diplome_formation_{census}_libcom_idx ON insee.diplome_formation_{census} USING btree (libcom);


COMMENT ON TABLE insee.diplome_formation_{census} IS 'Diplôme formation à l''IRIS (source Insee), census {census}';

COMMENT ON COLUMN insee.diplome_formation_{census}.iris IS 'IRIS';
COMMENT ON COLUMN insee.diplome_formation_{census}.reg IS 'Région (nouvelle)';
COMMENT ON COLUMN insee.diplome_formation_{census}.dep IS 'Département';
COMMENT ON COLUMN insee.diplome_formation_{census}.uu2010 IS 'Unité urbaine';
COMMENT ON COLUMN insee.diplome_formation_{census}.com IS 'Commune ou ARM';
COMMENT ON COLUMN insee.diplome_formation_{census}.libcom IS 'Libellé commune ou ARM';
COMMENT ON COLUMN insee.diplome_formation_{census}.triris IS 'TRIRIS';
COMMENT ON COLUMN insee.diplome_formation_{census}.grd_quart IS 'Grand quartier';
COMMENT ON COLUMN insee.diplome_formation_{census}.libiris IS 'Libellé de l''IRIS';
COMMENT ON COLUMN insee.diplome_formation_{census}.typ_iris IS 'Type d''IRIS';
COMMENT ON COLUMN insee.diplome_formation_{census}.modif_iris IS 'Modification de l''IRIS';
COMMENT ON COLUMN insee.diplome_formation_{census}.lab_iris IS 'Label de l''IRIS';

COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop0205 IS 'Pop 2-5 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop0610 IS 'Pop 6-10 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop1114 IS 'Pop 11-14 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop1517 IS 'Pop 15-17 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop1824 IS 'Pop 18-24 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop2529 IS 'Pop 25-29 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_pop30p IS 'Pop 30 ans ou plus en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol0205 IS 'Pop scolarisée 2-5 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol0610 IS 'Pop scolarisée 6-10 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol1114 IS 'Pop scolarisée 11-14 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol1517 IS 'Pop scolarisée 15-17 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol1824 IS 'Pop scolarisée 18-24 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol2529 IS 'Pop scolarisée 25-29 ans en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_scol30p IS 'Pop scolarisée 30 ans ou plus en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_nscol15p IS 'Pop 15 ans ou plus non scolarisée en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_nscol15p_diplmin IS 'Pop 15 ans ou plus non scol. Sans diplôme ou CEP en 2017 (princ)';
--ajout nouvelle version du fichier
COMMENT ON COLUMN insee.diplome_formation_{census}.P_NSCOL15P_BEPC IS 'Pop 15 ans ou plus non scol. BEPC, brevet des collèges, DNB en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_nscol15p_capbep IS 'Pop 15 ans ou plus non scol. CAP-BEP en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_nscol15p_bac IS 'Pop 15 ans ou plus non scol. BAC en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_NSCOL15P_SUP2 IS 'Pop 15 ans ou plus non scol. Enseignement sup de niveau bac + 2 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_NSCOL15P_SUP34 IS 'Pop 15 ans ou plus non scol. Enseignement sup de niveau bac + 3 ou 4 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_NSCOL15P_SUP5 IS 'Pop 15 ans ou plus non scol. Enseignement sup de niveau bac + 5 ou plus en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_hnscol15p IS 'Hommes 15 ans ou plus non scolarisés en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_hnscol15p_diplmin IS 'Hommes 15 ans ou plus non scol. Sans diplôme ou CEP en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_HNSCOL15P_BEPC IS 'Hommes 15 ans ou plus non scol. BEPC, brevet des collèges, DNB en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_hnscol15p_capbep IS 'Hommes 15 ans ou plus non scol. CAP-BEP ou equiv en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_hnscol15p_bac IS 'Hommes 15 ans ou plus non scol. BAC en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_HNSCOL15P_SUP2 IS 'Hommes 15 ans ou plus non scol. Enseignement sup de niveau bac + 2 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_HNSCOL15P_SUP34 IS 'Hommes 15 ans ou plus non scol. Enseignement sup de niveau bac + 3 ou 4 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_HNSCOL15P_SUP5 IS 'Hommes 15 ans ou plus non scol. Enseignement sup de niveau bac + 5 ou plus en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_fnscol15p IS 'Femmes 15 ans ou plus non scolarisées en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_fnscol15p_diplmin IS 'Femmes 15 ans ou plus non scol. Sans diplôme ou CEP en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_FNSCOL15P_BEPC IS 'Femmes 15 ans ou plus non scol. BEPC, brevet des collèges, DNB en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_fnscol15p_capbep IS 'Femmes 15 ans ou plus non scol. CAP-BEP en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.p_fnscol15p_bac IS 'Femmes 15 ans ou plus non scol. BAC en  2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_FNSCOL15P_SUP2 IS 'Femmes 15 ans ou plus non scol. Enseignement sup de niveau bac + 2 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_FNSCOL15P_SUP34 IS 'Femmes 15 ans ou plus non scol. Enseignement sup de niveau bac + 3 ou 4 en 2017 (princ)';
COMMENT ON COLUMN insee.diplome_formation_{census}.P_FNSCOL15P_SUP5 IS 'Femmes 15 ans ou plus non scol. Enseignement sup de niveau bac + 5 ou plus en 2017 (princ)';


\copy insee.diplome_formation_{census} FROM '{fpath}' DELIMITER '{sep}' CSV HEADER;
