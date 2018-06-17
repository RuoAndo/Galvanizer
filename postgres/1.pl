#!/usr/bin/perl -w

#use DateTime;
#my $dt = DateTime->now( time_zone=>'local' );
my $filein = $ARGV[0];

open(FILEHANDLE, $filein);
@list = <FILEHANDLE>;

$counter = 1;

foreach $data (@list)
{

  #flist:
    #libxl_domain_info  372 tools/libxl/libxl.c int libxl_domain_info(libxl_ctx *ctx, 
    #libxl_dominfo *info_r,                                                                          #libxl_list_cpupool  388 tools/libxl/libxl.c 
    #libxl_cpupoolinfo * libxl_list_cpupool(libxl_ctx *ctx, int *nb_pool) 

  # python 1.py tools/libxl/libxl.c libxl 372

    @m = split(/\s+/,$data);

    #print $m[0]."\n";
    #print $m[1]."\n";
    #print $m[2]."\n";
    
    $result=`python 1.py $m[2] $m[0] $m[1]`;
    print $result;

    $counter++;

}

close(FILEHANDLE);
