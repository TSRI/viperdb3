query = """SELECT t5.AI,t5.SI,t5.CI,t5.Num_Atoms,t5.SST,t5.r,t5.phi,t5.psi,t5.eff_rad,t5.dSASAU,t5.SASA,t8.VM,t8.Num_Int,t5.Cons,t5.TAE,t5.TSE,t5.TBSA
FROM (
  SELECT t9.AI,t9.SI,t9.CI,t9.Num_Atoms,t9.SST,t9.Cons,t9.r,t9.phi,t9.psi,t9.eff_rad,t9.dSASAU,t9.SASA,t10.TAE,t10.TSE,t10.TBSA
  FROM (
    SELECT t3.AI,t3.SI,t3.CI,t3.Num_Atoms,t3.SST,t3.Cons,t3.r,t3.phi,t3.psi,t4.eff_rad,t4.dSASAU,t4.SASA 
    FROM (
      SELECT t1.SI,t1.AI,t1.CI,t1.Num_Atoms,t2.SST,t2.Cons,t1.r,t1.phi,t1.psi 
      FROM (
        SELECT  v.auth_seq_id AS SI, v.label_asym_id AS AI, v.auth_comp_id AS CI, count(v.label_seq_id) AS Num_Atoms,
          round(sqrt((avg(v.cartn_x)*avg(v.cartn_x))+(avg(v.cartn_y)*avg(v.cartn_y))+(avg(v.cartn_z)*avg(v.cartn_z)))) AS r,
          round(atan2(avg(v.cartn_y),avg(v.cartn_x))*(180.0/(4.0*atan2(1.0,1.0)))) AS phi,
          round(acos(avg(v.cartn_z)/(sqrt((avg(v.cartn_x)*avg(v.cartn_x))+(avg(v.cartn_y)*avg(v.cartn_y))+(avg(v.cartn_z)*avg(v.cartn_z)))))*(180.0/(4.0*atan2(1.0,1.0)))) AS psi,
          round(avg(v.cartn_x)) AS X, round(avg(v.cartn_y)) AS Y, round(avg(v.cartn_z)) AS Z
        FROM virus_atom_site v
        WHERE v.entry_key=%(entry_key)d AND v.label_asym_id='%(label_asym_id)s'
        GROUP BY v.auth_seq_id, v.label_asym_id, v.auth_comp_id 
        ORDER BY v.label_asym_id, v.auth_seq_id
      ) t1
      LEFT JOIN (
        SELECT v.label_seq_id AS SI, v.structure AS SST, v.conservation AS Cons 
        FROM virus_residue_stride v 
        WHERE v.entry_id='%(entry_id)s' AND v.label_asym_id='%(label_asym_id)s'
      ) t2
      ON t1.SI=t2.SI
    ) t3
    LEFT JOIN (
      SELECT v.label_seq_id AS SI,v.label_asym_id AS AI, v.label_comp_id AS CI,
        round((v.radius_aa - (SELECT MIN(v.radius_aa) FROM virus_residue_asa v WHERE v.entry_key=%(entry_key)d AND v.label_asym_id='%(label_asym_id)s')),0) AS eff_rad,
        round((v.sasa_unbound/v.sasa_reference_aa),2) AS dSASAU,
        round(v.sasa_bound,2) AS SASA
      FROM virus_residue_asa v 
      WHERE v.entry_key=%(entry_key)d AND v.label_asym_id='%(label_asym_id)s' 
      ORDER BY v.label_seq_id
    ) t4
    ON t3.SI=t4.SI
  ) t9
 LEFT JOIN (
    SELECT t11.SI, SUM(t11.AE) AS TAE, SUM(t11.SE) AS TSE, SUM(t11.BSA) AS TBSA
    FROM (
         (
      SELECT v.auth_1_comp_id AS CI, v.auth_1_seq_id AS SI, v.auth_1_asym_id AS AI1, v.auth_2_asym_id AS AI2, v.viper_matrix_1 AS VM1, v.viper_matrix_2 AS VM2, v.association_nrg AS AE, v.solvation_nrg AS SE, v.bsa AS BSA, v.ordering AS O
      FROM virus_residue_energy v 
      WHERE v.entry_key=%(entry_key)d AND v.auth_1_asym_id='%(subunit)s' AND v.auth_2_asym_id NOT IN ('R','S','T') AND v.ordering=1
      ORDER BY v.auth_1_seq_id
         )
         UNION ALL
         (
      SELECT v.auth_1_comp_id AS CI, v.auth_1_seq_id AS SI, v.auth_1_asym_id AS AI1, v.auth_2_asym_id AS AI2, v.viper_matrix_1 AS VM1, v.viper_matrix_2 AS VM2, v.association_nrg AS AE, v.solvation_nrg AS SE, v.bsa AS BSA, v.ordering AS O
      FROM virus_residue_energy v 
      WHERE v.entry_key=%(entry_key)d AND v.auth_2_asym_id='%(subunit)s' AND v.auth_1_asym_id NOT IN ('R','S','T') AND v.ordering=2
      ORDER BY v.auth_1_seq_id
         )
    ) t11
    GROUP BY t11.SI
  ) t10
  ON t9.SI=t10.SI
) t5
LEFT JOIN (
  SELECT t6.SI, t6.AI, count(t6.VM) as VM, count(distinct(t6.insi)) as Num_Int
  FROM (
    (
      SELECT v.auth_1_seq_id AS SI, v.auth_1_asym_id AS AI, v.viper_matrix_1 AS VM,
      v.auth_2_seq_id AS INSI, v.auth_2_asym_id AS INAI, v.viper_matrix_2 AS INVM 
      FROM virus_residue_contact v 
      WHERE v.entry_id='2ms2' AND v.auth_1_asym_id NOT IN ('R','S','T') AND v.auth_1_asym_id='C' AND v.auth_2_comp_id NOT IN ('GUA','ADE','URA','CYT','THY')
      ORDER BY v.viper_matrix_1, v.auth_1_asym_id, v.auth_1_seq_id
    )
    UNION ALL
    (
        SELECT v.auth_2_seq_id AS SI, v.auth_2_asym_id AS AI, v.viper_matrix_2 AS VM,
        v.auth_1_seq_id AS INSI, v.auth_1_asym_id AS INAI, v.viper_matrix_1 AS INVM 
        FROM virus_residue_contact v 
        WHERE v.entry_id='2ms2' AND v.auth_1_asym_id NOT IN ('R','S','T') AND v.auth_2_asym_id='C' AND v.auth_1_comp_id NOT IN ('GUA','ADE','URA','CYT','THY')
        ORDER BY v.viper_matrix_2, v.auth_2_asym_id, v.auth_2_seq_id
    )
  ) t6
  GROUP BY t6.SI, t6.AI
) t8
ON t5.SI=t8.SI
%(sic)s
ORDER BY %(order_by)s
LIMIT %(limit)d"""

PHI_PSI = ' '.join(map(lambda line: line.strip(), query.split('\n')))

ORDER_BY = {
  "ASSENE":  "t5.TAE",
  "SOLVENE": "t5.TSE",
  "BSA":     "t5.TBSA",
  "SASA":    "t5.SASA",
  "RID":     "t5.SI+0"
}

SIC_core_threshold = 0.05
SIC_surf_threshold = 10

cons = False
#TODO get cons
CONS = "AND t5.Cons='*'" if cons else ""
SELECT_SIC_GROUP = {
  "CORE":      "WHERE t8.VM IS NULL AND t5.dSASAU <= %d AND t5.eff_rad >=0" % (SIC_core_threshold),
  "SURFOUT":   "WHERE t8.VM IS NULL AND t5.dSASAU > %d AND t5.eff_rad > %d" % (SIC_core_threshold, SIC_surf_threshold),
  "SURFIN":    "WHERE t8.VM IS NULL AND t5.dSASAU > %d AND t5.eff_rad<= %d" % (SIC_core_threshold, SIC_surf_threshold),
  "INTERFACE": "WHERE t8.VM IS NOT NULL %s" % (CONS),
}

def phi_psi_query(virus_dict):
  virus_dict["order_by"] = ORDER_BY[virus_dict["order_by"]]
  virus_dict["sic"] = SELECT_SIC_GROUP[virus_dict["sic"]]

  return PHI_PSI % virus_dict

