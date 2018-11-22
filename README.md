# lrg_parser


# MISC notes
 Selecting first transcript
 From root:
 transcript_elem = root.find('transcript')

 Mapping coords from LRG files
 In annotation_set type='lrg'
 <mapping coord_system="GRCH...". Should start with 37 or 38 depending on input flag? Default to 38
 other_name is chromsome number
 in <mapping_span> (should only be 1 for grch mapping coord); VALUE TO ADD TO LRG NUMBERS TO TRANSLATE IS: transval = 
   lrg_end - lrg_start. Should assert that: other_start + transval = other_end
   use other_start and other_end and strand for bedfile.

 Name bedfile according to LRG_HGNCID_GRCH.bed
 lrg num is in <fixed_annotation><id>
 HGNC id is in lrg_locus text
 GRCH is in <mapping coord_system= of the lrg ?

 overlapping exons from multiple transcripts differentiated by a letter suffix eg 14a/14b in LRG_5
 Exons are unique. See FAQ: Each exon is numbered consecutively 5′ to 3′; the numbering is then applied to individual transcripts.

 Opening to a genome browser page:
 UCSC: http://genome-euro.ucsc.edu/cgi-bin/hgTracks?org=hum&db=hg19&position=chr17:48259457-48284000  or use position=lrg_4;replace hg19 with hg38 for grch38
 ENSEMBL: http://grch37.ensembl.org/Homo_sapiens/Location/View?r=17:48259457-48284000  or g=lrg_num; replace grch37 with www for grch38
 Looking at the difference searching manually and with xml links, it seems like the LRG is padded by 5000. All 
' Biostars mention of this, and all transcript 1s start at 5001.:
"The purpose of LRGs is to be independent of genomes. It has no chromosomal location, it is its own location. Their coordinates are, therefore, themselves + 5kb upstream, allowing you to map variants to them and their likely regulatory regions. Have a look at some more LRGs, they all have themselves as the coordinate system name and they all have a start coordinate of 5001."
    !! Interesting. This use case for the project is pointless. LRGs are made to be MAPPED TO. Not tranlsated to reference coordinates.

 Downloading XML file:
 wget http://ftp.ebi.ac.uk/pub/databases/lrgex/LRG_3.xml

 Remapping coordinates with NCBI
 https://www.ncbi.nlm.nih.gov/genome/tools/remap/docs/api