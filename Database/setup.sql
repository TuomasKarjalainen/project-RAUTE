USE Projekti;

CREATE TABLE VerifiedPairs (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     dfile VARCHAR(255),
     pfile VARCHAR(255),
     PRIMARY KEY (id)
 ); 

CREATE TABLE PreprocessedData (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     peelFile VARCHAR(255),
	 dryFile VARCHAR(255),
	 m_uWidth FLOAT,
	 m_uLength FLOAT,
	 m_dThickness FLOAT,
	 B1MoistureAvg FLOAT,
	 B1TemperatureAvg FLOAT,
	 B1DensityAvg FLOAT,
	 B1KnotCount FLOAT,
	 B1KnotWidthSum FLOAT,
	 B1DecayCount FLOAT,
	 B1DecayWidthSum FLOAT,
	 B1AllOtherDefectCount FLOAT,
	 B1AllOtherDefectWidthSum FLOAT,
	 B2MoistureAvg FLOAT,
	 B2TemperatureAvg FLOAT,
	 B2DensityAvg FLOAT,
	 B2KnotCount FLOAT,
	 B2KnotWidthSum FLOAT,
	 B2DecayCount FLOAT,
	 B2DecayWidthSum FLOAT,
	 B2AllOtherDefectCount FLOAT,
	 B2AllOtherDefectWidthSum FLOAT,
	 B3MoistureAvg FLOAT,
	 B3TemperatureAvg FLOAT,
	 B3DensityAvg FLOAT,
	 B3KnotCount FLOAT,
	 B3KnotWidthSum FLOAT,
	 B3DecayCount FLOAT,
	 B3DecayWidthSum FLOAT,
	 B3AllOtherDefectCount FLOAT,
	 B3AllOtherDefectWidthSum FLOAT,
	 B4MoistureAvg FLOAT,
	 B4TemperatureAvg FLOAT,
	 B4DensityAvg FLOAT,
	 B4KnotCount FLOAT,
	 B4KnotWidthSum FLOAT,
	 B4DecayCount FLOAT,
	 B4DecayWidthSum FLOAT,
	 B4AllOtherDefectCount FLOAT,
	 B4AllOtherDefectWidthSum FLOAT,
	 B5MoistureAvg FLOAT,
	 B5TemperatureAvg FLOAT,
	 B5DensityAvg FLOAT,
	 B5KnotCount FLOAT,
	 B5KnotWidthSum FLOAT,
	 B5DecayCount FLOAT,
	 B5DecayWidthSum FLOAT,
	 B5AllOtherDefectCount FLOAT,
	 B5AllOtherDefectWidthSum FLOAT,
	 B6MoistureAvg FLOAT,
	 B6TemperatureAvg FLOAT,
	 B6DensityAvg FLOAT,
	 B6KnotCount FLOAT,
	 B6KnotWidthSum FLOAT,
	 B6DecayCount FLOAT,
	 B6DecayWidthSum FLOAT,
	 B6AllOtherDefectCount FLOAT,
	 B6AllOtherDefectWidthSum FLOAT,
	 B7MoistureAvg FLOAT,
	 B7TemperatureAvg FLOAT,
	 B7DensityAvg FLOAT,
	 B7KnotCount FLOAT,
	 B7KnotWidthSum FLOAT,
	 B7DecayCount FLOAT,
	 B7DecayWidthSum FLOAT,
	 B7AllOtherDefectCount FLOAT,
	 B7AllOtherDefectWidthSum FLOAT,
	 B8MoistureAvg FLOAT,
	 B8TemperatureAvg FLOAT,
	 B8DensityAvg FLOAT,
	 B8KnotCount FLOAT,
	 B8KnotWidthSum FLOAT,
	 B8DecayCount FLOAT,
	 B8DecayWidthSum FLOAT,
	 B8AllOtherDefectCount FLOAT,
	 B8AllOtherDefectWidthSum FLOAT,
	 B9MoistureAvg FLOAT,
	 B9TemperatureAvg FLOAT,
	 B9DensityAvg FLOAT,
	 B9KnotCount FLOAT,
	 B9KnotWidthSum FLOAT,
	 B9DecayCount FLOAT,
	 B9DecayWidthSum FLOAT,
	 B9AllOtherDefectCount FLOAT,
	 B9AllOtherDefectWidthSum FLOAT,
	 dryWidth FLOAT,
	 dryMoisturePercentage FLOAT,
     PRIMARY KEY (id)
 ); 



LOAD DATA INFILE '/home/VerifiedPairs.csv' INTO TABLE VerifiedPairs FIELDS TERMINATED BY ';';