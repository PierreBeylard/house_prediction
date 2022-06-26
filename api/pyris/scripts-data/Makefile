# Retrieve the filename from an URL
# Param:
#   1. parsed string with the form 'https://website.jazz/path/to/file.zip'.
url2file = $(lastword $(subst /, ,$1))

# Downloading folder
DOWNLOADDIR=download
# Folder to process some data
DATADIR=data


IGN_URL=ftp://Contours_IRIS_ext:ao6Phu5ohJ4jaeji@ftp3.ign.fr/CONTOURS-IRIS_2-1__SHP__FRA_2021-01-01.7z
IGN_ZIP_FILE=contour-iris.7z
IGN_REFERENCE_SHAPEFILE=CONTOURS-IRIS_2-1__SHP__FRA_2021-01-01/CONTOURS-IRIS/1_DONNEES_LIVRAISON_2021-06-00217/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2021/CONTOURS-IRIS.shp

IGN_SHAPEFILE=$(addsuffix -metropole-2021Q.shp, $(basename $(notdir $(IGN_REFERENCE_SHAPEFILE))))

# Insee Data : IRIS 2021 and census 2018 (IRIS)
INSEE_URL=https://www.insee.fr/fr/statistiques/fichier/2017499/reference_IRIS_geo2021.zip
INSEE_ZIP_FILE=iris-insee-2021.zip
INSEE_REFERENCE_FILE=reference_IRIS_geo2021.xlsx
INSEE_INFRA_URLS := https://www.insee.fr/fr/statistiques/fichier/4799309/base-ic-evol-struct-pop-2017.zip \
	https://www.insee.fr/fr/statistiques/fichier/5650714/base-ic-couples-familles-menages-2018.zip \
	https://www.insee.fr/fr/statistiques/fichier/4799305/base-ic-logement-2017.zip \
	https://www.insee.fr/fr/statistiques/fichier/4799252/base-ic-diplomes-formation-2017.zip \
	https://www.insee.fr/fr/statistiques/fichier/4799323/base-ic-activite-residents-2017.zip \


# French national addresses data
BAN_URL = http://bano.openstreetmap.fr/data/full.sjson.gz
BAN_ZIP_FILE = $(call url2file, $(BAN_URL))
BAN_FILE = $(addprefix bano-, $(subst .gz,, $(BAN_ZIP_FILE)))

# File list to download
# Loop on ech url to retrieve the .zip filename
INSEE_INFRA_ZIPFILES := $(foreach url, $(INSEE_INFRA_URLS), $(DOWNLOADDIR)/$(call url2file, $(url)))
# Loop on each .zip file and then replace .zip by .xls. From the 'download' folder to the 'data' folder.
INSEE_INFRA_FILES := $(subst $(DOWNLOADDIR)/,$(DATADIR)/, $(subst .zip,.xls, $(INSEE_INFRA_ZIPFILES)))
# .xls files to .csv
INSEE_INFRA_CSV := $(subst .xls,.csv, $(INSEE_INFRA_FILES))
# $(info INSEE_INFRA_FILES IS $(INSEE_INFRA_FILES))
# $(info INSEE_INFRA_CSV IS $(INSEE_INFRA_CSV))


# Before removing the folder content, check the variables DATADIR et
# DOWNLOADDIR. They must exist and be non empty.
ifndef DATADIR
$(error DATADIR is not set)
endif

ifndef DOWNLOADDIR
$(error DOWNLOADDIR is not set)
endif

.PHONY: all
all: download unzip copydatadir tocsv

.PHONY: download
download: $(DOWNLOADDIR)/$(IGN_ZIP_FILE) $(DOWNLOADDIR)/$(INSEE_ZIP_FILE) $(INSEE_INFRA_ZIPFILES) $(DOWNLOADDIR)/$(BAN_ZIP_FILE)

.PHONY: unzip
unzip: $(DOWNLOADDIR)/$(INSEE_REFERENCE_FILE) $(DOWNLOADDIR)/$(IGN_REFERENCE_SHAPEFILE) $(INSEE_INFRA_FILES)

.PHONY: copydatadir
copydatadir: $(DATADIR)/insee-iris.xlsx $(DATADIR)/$(IGN_SHAPEFILE) $(DATADIR)/$(BAN_FILE)

.PHONY: tocsv
tocsv: $(DATADIR)/insee-iris.csv $(INSEE_INFRA_CSV)

.PHONY: clean
clean: cleandata cleandownload

.PHONY: cleandata
cleandata:
	rm -f $(DATADIR)/*

.PHONY: cleandownload
cleandownload:
	rm -rf $(DOWNLOADDIR)/*


# Allow you to loop on all URLs (Insee) and generate as many URLS as targets. The
# target will be infer from the name of the file.
include downloads.mk

downloads.mk: Makefile
	@rm -f $@
	@for f in $(INSEE_INFRA_URLS); do \
                _dir=$(DOWNLOADDIR) ; \
		out=`echo $$f | awk -F "/" '{print $$NF}'`; \
                echo -e "$$_dir/$$out: \n\twget $$f -O \$$@\n\n" >> $@; \
        done


# IGN File
$(DOWNLOADDIR)/$(IGN_ZIP_FILE):
	mkdir -p $(dir $@)
	echo $(dir $@)
	echo '$(IGN_URL)'
	wget '$(IGN_URL)' -O $@

$(DOWNLOADDIR)/$(IGN_REFERENCE_SHAPEFILE): $(DOWNLOADDIR)/$(IGN_ZIP_FILE)
	7z x -stl -o$(DOWNLOADDIR) $<

# copy all files with the same stem of the .shp file (.prf, .dbf) etc.
$(DATADIR)/$(IGN_SHAPEFILE): $(DOWNLOADDIR)/$(IGN_REFERENCE_SHAPEFILE)
	mkdir -p $(dir $@)
	# shapefile
	cp $< $@
	# other extensions : dbf, etc.
	cp $(addsuffix .cpg, $(basename $<)) $(addsuffix .cpg, $(basename $@))
	cp $(addsuffix .dbf, $(basename $<)) $(addsuffix .dbf, $(basename $@))
	cp $(addsuffix .prj, $(basename $<)) $(addsuffix .prj, $(basename $@))
	cp $(addsuffix .shx, $(basename $<)) $(addsuffix .shx, $(basename $@))


# Address data
$(DOWNLOADDIR)/$(BAN_ZIP_FILE):
	wget '$(BAN_URL)' -O $@

# Unzip files into the 'data' folder
$(DATADIR)/$(BAN_FILE): $(DOWNLOADDIR)/$(BAN_ZIP_FILE)
	gzip -c -d $< > $@


# Insee IRIS files
$(DOWNLOADDIR)/$(INSEE_ZIP_FILE):
	mkdir -p $(dir $@)
	wget '$(INSEE_URL)' -O $@

$(DOWNLOADDIR)/$(INSEE_REFERENCE_FILE): $(DOWNLOADDIR)/$(INSEE_ZIP_FILE)
	unzip -DD $< -d $(DOWNLOADDIR)

# Insee IRIS data
$(DATADIR)/insee-iris.xlsx: $(DOWNLOADDIR)/$(INSEE_REFERENCE_FILE)
	mkdir -p $(dir $@)
	cp $< $@

# Convert Excel files into a CSV files thanks to csvkit
$(DATADIR)/insee-iris.csv: $(DATADIR)/insee-iris.xlsx
	PYTHONIOENCODING=utf8 in2csv -e LATIN1 --sheet Emboitements_IRIS -K 5 $(subst .csv,.xlsx,$@) > $@

# Some other Insee files. Unzip files from 'download' into the 'data' folder
$(INSEE_INFRA_FILES): $(INSEE_INFRA_ZIPFILES)
	unzip -DD $(subst $(DATADIR)/,$(DOWNLOADDIR)/, $(subst .xls,.zip,$@)) -d $(DATADIR)

# Convert Excel files into a CSV files thanks to csvkit
$(INSEE_INFRA_CSV): $(INSEE_INFRA_FILES)
	PYTHONIOENCODING=utf8 in2csv -e LATIN1 --sheet IRIS -K 5 $(subst .csv,.xlsx,$@) > $@
