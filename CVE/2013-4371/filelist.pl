#!/usr/bin/perl -w

#use DateTime;
#my $dt = DateTime->now( time_zone=>'local' );
my $filein = $ARGV[0];

open(FILEHANDLE, $filein);
@list = <FILEHANDLE>;

foreach $data (@list)
{
    @m = split(/\s+/,$data);

    print $m[2]."\n";

}

close(FILEHANDLE);
