#!/usr/bin/perl -w

#use DateTime;
#my $dt = DateTime->now( time_zone=>'local' );
my $filein = $ARGV[0];

open(FILEHANDLE, $filein);
@list = <FILEHANDLE>;

$counter = 1;

foreach $data (@list)
{
    @m = split(/\,/,$data);

    #print $m[2]."\n";
    #$m[2]=~ s/\//_/g;
    #$m[2]=~ s/\./__/g;

    print $m[0]."\n";

    #print "break ".$m[2].":".$m[1]."\n";
        
    $counter++;

}

close(FILEHANDLE);
