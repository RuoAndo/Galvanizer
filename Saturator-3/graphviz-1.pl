#!/usr/bin/perl -w

#use DateTime;
#my $dt = DateTime->now( time_zone=>'local' );
my $filein = $ARGV[0];

open(FILEHANDLE, $filein);
@list = <FILEHANDLE>;

$counter = 0;

#print "digraph { \n";
#print "layout = \"fdp\" \n";

print "edge \[penwidth\=5 color\=green]\;\n";
#print "edge [penwidth = 5 color=red]\;";

foreach $data (@list)
{
    if($data =~ /_id/)
    {
	#print $data;
    
	my @m = split /"caller_name"/, $data;
	#print $m[1]."\n";

	my @n = split /\s/, $m[1];
	$n[2] =~ s/\"//g;
	#print $n[2]."\n";

	if($n[2] eq "main")
	{
	    print "edge \[penwidth\=5 color\=red]\;\n";
	    print "xc_domain_getinfo ->".$n[2]."\n";
	}
	else
	{
	    print "edge \[penwidth\=5 color\=green]\;\n";
	    print "xc_domain_getinfo ->".$n[2]."\n";
	}
    }

}

#print "}\n";

close(FILEHANDLE);
