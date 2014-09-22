/*
This module is for storing microbial growth phenotype data, e.g., from
FEBA or ENIGMA
*/

module KBaseGrowthPhenotype {
    
/*
@id ws KBaseGenomes.Genome
*/
typedef string GenomeID;

/*
@id ws KBaseGenomes.Contig;
*/
typedef string ContigID;

/*
@id ws KBaseCommunities.Sample;
*/
typedef string SampleID;

/*
@id ws KBaseBiochem.Media;
*/
typedef string MediaID;

/*
should this be linked to KBaseGenomes.Feature with an @id tag?
*/
typedef string FeatureID;

/*
Not sure if this is still needed; must be 0 or 1
*/
typedef int Boolean;

/*
enum: insertion, deletion, substitution
The latter is not strictly necessary, but convenient to avoid storing
two separate events.
*/
typedef string ChangeType;

/*
  A Delta is a description of a single change to a strain.  A series
  of Deltas defines the transition from one Strain to another.  For
  sequenced insertions or substitutions, give the 0-indexed position
  on the contig where the insertion/substitution begins, in the +
  direction.  For sequenced deletions and substitutions, give the
  position and length.  The position of all Deltas should be
  calculated relative to the parent strain (derived_from_strain), so
  that the Deltas could be applied in any order.
@optional change_type feature_id contig_id sequence position length
*/
typedef structure {
    string description;
    ChangeType change_type;
    FeatureID feature_id;
    ContigID contig_id;
    string sequence;
    int position;
    int length;
} Delta;

/*
@id ws KBaseGrowthPhenotype.Strain
*/
typedef string StrainID;

/*
  A Strain is a particular genetic variant of an organism.  Optionally,
  it may be:
    * derived from another Strain (e.g., as an engineered mutant)
    * sequenced
    * isolated from a community
    * a wild-type example of a Genome
  If a strain is "wild type" it should have a non-null genome_id and a
  null derived_from_strain.  If not wild type, genome_id should be
  set to the "original" parent strain in KBase, if it exists, or null
  if it does not exist or is unknown.
@optional description genome_id derived_from_strain deltas isolated_from
*/
typedef structure {
    string name;
    string description;
    GenomeID genome_id;
    StrainID derived_from_strain;
    list<Delta> deltas;
    SampleID isolated_from;
} Strain;

/*
@id ws KBaseGrowthPhenotype.Pool
*/
typedef string PoolID;

/*
  A Pool is a collection of barcoded strains.  Barcodes, tags, etc should
  be stored as Deltas in each strain.
@optional comments
*/
typedef structure {
    string name;
    string comments;
    list<Strain> strains;
} Pool;

/*
  A Condition is something that's added to particular aliquots in
  a growth experiment, in addition to the media.  e.g., it may be a stress
  condition, or a nutrient.
@optional concentration units
*/
typedef structure {
    string name;
    float concentration;
    string units;
} Condition;

/*
  GrowthParameters describes all the conditions a particular aliquot
  was subjected to in an experiment
@optional person description gDNA_plate gDNA_well index media_id growth_method group temperature pH isLiquid isAerobic shaking conditions growth_plate_id growth_plate_wells startOD endOD total_generations
*/
typedef structure {
    string person;
    string description;
    string gDNA_plate;
    string gDNA_well;
    string index;
    MediaID media_id;
    string growth_method;
    string group;
    float temperature;
    float pH;
    Boolean isLiquid;
    Boolean isAerobic;
    string shaking;
    list<Condition> conditions;
    string growth_plate_id;
    string growth_plate_wells;
    float startOD;
    float endOD;
    float total_generations;
} GrowthParameters;

/*
@id ws KBaseGrowthPhenotype.GrowthParameters
*/
typedef string GrowthParametersID;

/*
  A TnSeqExperiment is an experiment in which a pool of mutants is created 
  by a transposone mutagenesis.
*/
typedef structure {
	string name;
	PoolID pool_id;
	string start_date;
	string sequenced_at;
	GrowthParametersID growth_parameter;
} TnSeqExperiment;

/*
@id ws KBaseGrowthPhenotype.TnSeqExperiment
*/
typedef string TnSeqExperimentID;

/*
  Number of strains determined from sequencing of TnSeq library.
*/
typedef tuple<StrainID,long> TnSeqResult;

/*
  TnSeqExperimentResults stores the results of sequencing of a TnSeq experiment, i.e. 
  number of times each mutant strain is detetcted from sequencing.
*/
typedef structure {
	TnSeqExperimentID experiment_id;
	list<TnSeqResult> results;
} TnSeqExperimentResults;

/*
@id ws KBaseGrowthPhenotype.TnSeqExperimentResults
*/
typedef string TnSeqExperimentResultsID;

/*
  TnSeqLibrary is a filtered subset of strains from TnSeqExperimentResults that is 
  suitable for the subsequent analysis of BarSeq experiments.
*/
typedef structure {
	TnSeqExperimentResultsID experiment_results_id;
	list<TnSeqResult> results;
} TnSeqLibrary;

/*
@id ws KBaseGrowthPhenotype.TnSeqLibrary
*/
typedef string TnSeqLibraryID;


/*
  A BarSeqExperiment is an experiment in which a pool is grown in
  several parallel aliquots (e.g., wells or tubes), each potentially
  treated with a different set of conditions
*/
typedef structure {
    string name;
    TnSeqLibraryID tnseq_library_id;
    string start_date;
    string sequenced_at;
    list<GrowthParametersID> growth_parameters;
} BarSeqExperiment;

/*
@id ws KBaseGrowthPhenotype.BarSeqExperiment
*/
typedef string BarSeqExperimentID;

/*
  Number of times a barcode (i.e. a strain) was detected by sequencing a pool at beginning (refernce state)
  and at the end of GrowthParameters, and a calculated log ratio of strain abundance relative to a starting
  condition.  
*/
typedef tuple<StrainID,GrowthParametersID,long,long,float> BarSeqResult;

/*
  BarSeqExperimentResults stores the log ratios calculated from
  a BarSeqExperiment.  There is one log ratio per strain per
  GrowthParameters.
*/
typedef structure {
    BarSeqExperimentID experiment_id;
    list<BarSeqResult> results;
} BarSeqExperimentResults;

}
