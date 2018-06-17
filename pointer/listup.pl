#!/usr/bin/perl
use File::Find;
use warnings;

#-- ディレクトリを指定(複数の指定可能) --#
@directories_to_search = ('./');

#-- 実行 --#
find(\&wanted, @directories_to_search);


 #--------------------------------------------
 #ファイルが見つかる度に呼び出される
 #--------------------------------------------
 sub wanted{
   $dir = $File::Find::dir, '/';    #カレントディレクトリ
   $sub = substr($dir,2);
   print $sub;

   print "/", $_;          #ファイル名

   print "\n";

   #フルパスのファイル名
   #print $File::Find::name, "\n";
 }

