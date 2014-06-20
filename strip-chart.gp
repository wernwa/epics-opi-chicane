set term png transparent
set output 'strip-chart-image'

plot 'strip-chart-data-01' with lines title 'data 01', \
    'strip-chart-data-02' with lines title 'data 02'
