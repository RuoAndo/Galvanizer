#!/usr/bin/perl
use File::Find;
use warnings;

#print $pwd;

#-- ディレクトリを指定(複数の指定可能) --#
@directories_to_search = ('./');

#-- 実行 --#
find(\&wanted, @directories_to_search);


 #--------------------------------------------
 #ファイルが見つかる度に呼び出される
 #--------------------------------------------
 sub wanted{
   #print $File::Find::dir, '/';    #カレントディレクトリ
   $pwd = `pwd`;
   chomp($pwd);
   print $pwd."/".$_;          #ファイル名
   print "\n";

   #フルパスのファイル名
   #print $File::Find::name, "\n";
 }

