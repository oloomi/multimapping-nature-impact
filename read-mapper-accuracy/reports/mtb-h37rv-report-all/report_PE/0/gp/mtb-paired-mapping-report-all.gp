
				set title "{/:Bold=16 mtb-paired-mapping-report-all}"

				set x2lab "FDR in mapping {{/:Italic(#wrongly mapped reads / #mapped reads)}}  "
				set log x
				set log x2

				set format x "10^{%L}"
				set format x2 "10^{%L}"
				set xran  [0.0000001000:0.0000100000]
				set x2ran [0.0000001000:0.0000100000]
				set x2tics
				unset xtics


				set ylab "Part of all reads (%)"

				set format y "%g %%"
				set yran [60.0000000000:100.0000000000]
				set y2ran [60.0000000000:100.0000000000]

				set pointsize 1.5

				set grid ytics lc rgb "#777777" lw 1 lt 0 front
				set grid x2tics lc rgb "#777777" lw 1 lt 0 front

				set datafile separator "	"
				set palette negative

				set termin svg size 640,640 enhanced
				set out "report_PE/0/svg/mtb-paired-mapping-report-all.svg"
				set key spacing 0.8 opaque width -5
				plot \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($6+$7+$8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#ee82ee" with filledcurve x1 title "Unmapped correctly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($7+$8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#ff0000" with filledcurve x1 title "Unmapped incorrectly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#00ff00" with filledcurve x1 title "Thresholded correctly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#008800" with filledcurve x1 title "Thresholded incorrectly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($5+$4+$10+$3+$2)*100/$11) lt rgb "#ffff00" with filledcurve x1 title "Multimapped", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($4+$10+$3+$2)*100/$11) lt rgb "#7f7f7f" with filledcurve x1 title "Mapped, should be unmapped", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($3+$2)*100/$11) lt rgb "#000000" with filledcurve x1 title "Mapped to wrong position", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($2)*100/$11) lt rgb "#0000ff" with filledcurve x1 title "Mapped correctly", \


				set termin pdf enhanced size 10.0000000000cm,10.0000000000cm enhanced font 'Arial,12'
				set out "report_PE/0/pdf/mtb-paired-mapping-report-all.pdf"
				set key spacing 0.8 opaque width 0
				plot \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($6+$7+$8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#ee82ee" with filledcurve x1 title "Unmapped correctly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($7+$8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#ff0000" with filledcurve x1 title "Unmapped incorrectly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($8+$9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#00ff00" with filledcurve x1 title "Thresholded correctly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($9+$5+$4+$10+$3+$2)*100/$11) lt rgb "#008800" with filledcurve x1 title "Thresholded incorrectly", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($5+$4+$10+$3+$2)*100/$11) lt rgb "#ffff00" with filledcurve x1 title "Multimapped", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($4+$10+$3+$2)*100/$11) lt rgb "#7f7f7f" with filledcurve x1 title "Mapped, should be unmapped", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($3+$2)*100/$11) lt rgb "#000000" with filledcurve x1 title "Mapped to wrong position", \
"report_PE/0/roc/mtb-paired-mapping-report-all.roc" using (( (($3+$4)/($2+$3+$4)) )):(($2)*100/$11) lt rgb "#0000ff" with filledcurve x1 title "Mapped correctly", \

			