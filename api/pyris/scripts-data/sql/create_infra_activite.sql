-- activité résidents infra communale (IRIS)
DROP TABLE IF EXISTS insee.activite_{census};
CREATE TABLE IF NOT EXISTS insee.activite_{census} (
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
 P_POP1564 float ,
  P_POP1524 float ,
  P_POP2554 float ,
  P_POP5564 float ,
  P_H1564 float ,
  P_H1524 float ,
  P_H2554 float ,
  P_H5564 float ,
  P_F1564 float ,
  P_F1524 float ,
  P_F2554 float ,
  P_F5564 float ,
  P_ACT1564 float ,
  P_ACT1524 float ,
  P_ACT2554 float ,
  P_ACT5564 float ,
  P_HACT1564 float ,
  P_HACT1524 float ,
  P_HACT2554 float ,
  P_HACT5564 float ,
  P_FACT1564 float ,
  P_FACT1524 float ,
  P_FACT2554 float ,
  P_FACT5564 float ,
  P_ACTOCC1564 float ,
  P_ACTOCC1524 float ,
  P_ACTOCC2554 float ,
  P_ACTOCC5564 float ,
  P_HACTOCC1564 float ,
  P_HACTOCC1524 float ,
  P_HACTOCC2554 float ,
  P_HACTOCC5564 float ,
  P_FACTOCC1564 float ,
  P_FACTOCC1524 float ,
  P_FACTOCC2554 float ,
  P_FACTOCC5564 float ,
  P_CHOM1564 float ,
  P_CHOM1524 float ,
  P_CHOM2554 float ,
  P_CHOM5564 float ,
  P_HCHOM1564 float ,
  P_FCHOM1564 float ,
  P_INACT1564 float ,
  P_HINACT1564 float ,
  P_FINACT1564 float ,
  P_ETUD1564 float ,
  P_HETUD1564 float ,
  P_FETUD1564 float ,
  P_RETR1564 float ,
  P_HRETR1564 float ,
  P_FRETR1564 float ,
  P_AINACT1564 float ,
  P_HAINACT1564 float ,
  P_FAINACT1564 float ,
  C_ACT1564 float ,
  C_ACT1564_CS1 float ,
  C_ACT1564_CS2 float ,
  C_ACT1564_CS3 float ,
  C_ACT1564_CS4 float ,
  C_ACT1564_CS5 float ,
  C_ACT1564_CS6 float ,
  C_ACTOCC1564 float ,
  C_ACTOCC1564_CS1 float ,
  C_ACTOCC1564_CS2 float ,
  C_ACTOCC1564_CS3 float ,
  C_ACTOCC1564_CS4 float ,
  C_ACTOCC1564_CS5 float ,
  C_ACTOCC1564_CS6 float ,
  P_ACTOCC15P float ,
  P_HACTOCC15P float ,
  P_FACTOCC15P float ,
  P_SAL15P float ,
  P_HSAL15P float ,
  P_FSAL15P float ,
  P_NSAL15P float ,
  P_HNSAL15P float ,
  P_FNSAL15P float ,
  P_ACTOCC15P_TP float ,
  P_SAL15P_TP float ,
  P_HSAL15P_TP float ,
  P_FSAL15P_TP float ,
  P_NSAL15P_TP float ,
  P_SAL15P_CDI float ,
  P_SAL15P_CDD float ,
  P_SAL15P_INTERIM float ,
  P_SAL15P_EMPAID float ,
  P_SAL15P_APPR float ,
  P_NSAL15P_INDEP float ,
  P_NSAL15P_EMPLOY float ,
  P_NSAL15P_AIDFAM float ,
  P_ACTOCC15P_ILT1 float ,
  P_ACTOCC15P_ILT2P float ,
  P_ACTOCC15P_ILT2 float ,
  P_ACTOCC15P_ILT3 float ,
  P_ACTOCC15P_ILT4 float ,
  P_ACTOCC15P_ILT5 float ,
  C_ACTOCC15P float ,
  C_ACTOCC15P_PAS float ,
  C_ACTOCC15P_MAR float ,
  C_ACTOCC15P_VELO float ,
  C_ACTOCC15P_2ROUESMOT float ,
  C_ACTOCC15P_VOIT float ,
  C_ACTOCC15P_TCOM float 
);

create index activite_{census}_dep_idx ON insee.activite_{census} USING btree (dep);
create index activite_{census}_com_idx ON insee.activite_{census} USING btree (com);
create index activite_{census}_libcom_idx ON insee.activite_{census} USING btree (libcom);

COMMENT ON TABLE insee.activite_{census} IS 'Activité des résidents à l''IRIS (source Insee), census {census}';

COMMENT ON COLUMN insee.activite_{census}.iris IS 'IRIS';
COMMENT ON COLUMN insee.activite_{census}.reg IS 'Région (nouvelle)';
COMMENT ON COLUMN insee.activite_{census}.dep IS 'Département';
COMMENT ON COLUMN insee.activite_{census}.uu2010 IS 'Unité urbaine';
COMMENT ON COLUMN insee.activite_{census}.com IS 'Commune ou ARM';
COMMENT ON COLUMN insee.activite_{census}.libcom IS 'Libellé commune ou ARM';
COMMENT ON COLUMN insee.activite_{census}.triris IS 'TRIRIS';
COMMENT ON COLUMN insee.activite_{census}.grd_quart IS 'Grand quartier';
COMMENT ON COLUMN insee.activite_{census}.libiris IS 'Libellé de l''IRIS';
COMMENT ON COLUMN insee.activite_{census}.typ_iris IS 'Type d''IRIS';
COMMENT ON COLUMN insee.activite_{census}.modif_iris IS 'Modification de l''IRIS';
COMMENT ON COLUMN insee.activite_{census}.lab_iris IS 'Label de l''IRIS';

COMMENT ON COLUMN insee.activite_{census}.p_pop1564 IS 'Pop 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_pop1524 IS 'Pop 15-24 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_pop2554 IS 'Pop 25-54 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_pop5564 IS 'Pop 55-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_h1564 IS 'Pop 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_h1524 IS 'Pop 15-24 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_h2554 IS 'Pop 25-54 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_h5564 IS 'Pop 55-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_f1564 IS 'Pop 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_f1524 IS 'Pop 15-24 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_f2554 IS 'Pop 25-54 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_f5564 IS 'Pop 55-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_act1564 IS 'Actifs 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_act1524 IS 'Actifs 15-24 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_act2554 IS 'Actifs 25-54 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_act5564 IS 'Actifs 55-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hact1564 IS 'Actifs 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hact1524 IS 'Actifs 15-24 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hact2554 IS 'Actifs 25-54 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hact5564 IS 'Actifs 55-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fact1564 IS 'Actifs 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fact1524 IS 'Actifs 15-24 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fact2554 IS 'Actifs 25-54 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fact5564 IS 'Actifs 55-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc1564 IS 'Actifs occupés 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc1524 IS 'Actifs occupés 15-24 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc2554 IS 'Actifs occupés 25-54 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc5564 IS 'Actifs occupés 55-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hactocc1564 IS 'Actifs occupés 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hactocc1524 IS 'Actifs occupés 15-24 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hactocc2554 IS 'Actifs occupés 25-54 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hactocc5564 IS 'Actifs occupés 55-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_factocc1564 IS 'Actifs occupés 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_factocc1524 IS 'Actifs occupés 15-24 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_factocc2554 IS 'Actifs occupés 25-54 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_factocc5564 IS 'Actifs occupés 55-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_chom1564 IS 'Chômeurs 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_chom1524 IS 'Chômeurs 15-24 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_chom2554 IS 'Chômeurs 25-54 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_chom5564 IS 'Chômeurs 55-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hchom1564 IS 'Chômeurs 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fchom1564 IS 'Chômeurs 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_inact1564 IS 'Inactifs 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hinact1564 IS 'Inactifs 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_finact1564 IS 'Inactifs 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_etud1564 IS 'Elèv. Etud. Stag. non rémunérés 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hetud1564 IS 'Elèv. Etud. Stag. non rémunérés 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fetud1564 IS 'Elèv. Etud. Stag. non rémunérés 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_retr1564 IS 'Retraités Préretraités 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hretr1564 IS 'Retraités Préretraités 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fretr1564 IS 'Retraités Préretraités 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_ainact1564 IS 'Autres inactifs 15-64 ans (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hainact1564 IS 'Autres inactifs 15-64 ans Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fainact1564 IS 'Autres inactifs 15-64 ans Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564 IS 'Actifs 15-64 ans (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs1 IS 'Actifs 15-64 ans Agriculteurs exploitants (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs2 IS 'Actifs 15-64 ans Artisans, Comm., Chefs entr. (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs3 IS 'Actifs 15-64 ans Cadres, Prof. intel. sup. (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs4 IS 'Actifs 15-64 ans Prof. intermédiaires (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs5 IS 'Actifs 15-64 ans Employés (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_act1564_cs6 IS 'Actifs 15-64 ans Ouvriers (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564 IS 'Actifs occupés 15-64 ans (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs1 IS 'Actifs occ 15-64 ans Agriculteurs exploitants (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs2 IS 'Actifs occ 15-64 ans Artisans, Comm., Chefs entr. (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs3 IS 'Actifs occ 15-64 ans Cadres Prof. intel. sup. (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs4 IS 'Actifs occ 15-64 ans Prof. intermédiaires (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs5 IS 'Actifs occupés 15-64 ans Employés (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc1564_cs6 IS 'Actifs occupés 15-64 ans Ouvriers (compl)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p IS 'Actifs occupés 15 ans ou plus (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hactocc15p IS 'Actifs occupés 15 ans ou plus Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_factocc15p IS 'Actifs occupés 15 ans ou plus Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p IS 'Salariés 15 ans ou plus (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hsal15p IS 'Salariés 15 ans ou plus Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fsal15p IS 'Salariés 15 ans ou plus Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_nsal15p IS 'Non-salariés 15 ans ou plus (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hnsal15p IS 'Non-salariés 15 ans ou plus Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fnsal15p IS 'Non-salariés 15 ans ou plus Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_tp IS 'Actifs occ 15 ans ou plus TP (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_tp IS 'Salariés 15 ans ou plus TP (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_hsal15p_tp IS 'Salariés 15 ans ou plus TP Hommes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_fsal15p_tp IS 'Salariés 15 ans ou plus TP Femmes (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_nsal15p_tp IS 'Non-salariés 15 ans ou plus TP (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_cdi IS 'Salariés 15 ans ou plus Fonct publ, CDI (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_cdd IS 'Salariés 15 ans ou plus CDD (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_interim IS 'Salariés 15 ans ou plus Intérim (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_empaid IS 'Salariés 15 ans ou plus Emplois aidés (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_sal15p_appr IS 'Salariés 15 ans ou plus Apprentissage - Stage (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_nsal15p_indep IS 'Non-salariés 15 ans ou plus Indépendants (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_nsal15p_employ IS 'Non-salariés 15 ans ou plus Employeurs (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_nsal15p_aidfam IS 'Non-salariés 15 ans ou plus Aides familiaux (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt1 IS 'Actif occ 15 ans ou plus travaille commune résidence (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt2p IS 'Actif occ 15 ans ou plus travaille autre commune que commune résidence (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt2 IS 'Actif occ 15 ans ou plus travaille autre commune même dépt résidence (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt3 IS 'Actif occ 15 ans ou plus travaille autre dépt même région résidence (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt4 IS 'Actif occ 15 ans ou plus travaille autre région en métropole (princ)';
COMMENT ON COLUMN insee.activite_{census}.p_actocc15p_ilt5 IS 'Actif occ 15 ans ou plus travaille autre région hors métropole (princ)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p IS 'Actif occ 15 ans ou plus (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_pas IS 'Actif occ 15 ans ou plus pas de transport (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_mar IS 'Actif occ 15 ans ou plus marche à pied (compl)';
-- COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_drou IS 'Actif occ 15 ans ou plus deux roues (compl)';
-- test 
COMMENT ON COLUMN insee.activite_{census}.C_ACTOCC15P_VELO IS 'Actif occ 15 ans ou plus vélo (compl)';
COMMENT ON COLUMN insee.activite_{census}.C_ACTOCC15P_2ROUESMOT IS 'Actif occ 15 ans ou plus 2 roues motorisées (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_voit IS 'Actif occ 15 ans ou plus voiture, camion (compl)';
-- fin tests
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_voit IS 'Actif occ 15 ans ou plus voiture, camion (compl)';
COMMENT ON COLUMN insee.activite_{census}.c_actocc15p_tcom IS 'Actif occ 15 ans ou plus transport en commun (compl)';


\copy insee.activite_{census} FROM '{fpath}' DELIMITER '{sep}' CSV HEADER;
