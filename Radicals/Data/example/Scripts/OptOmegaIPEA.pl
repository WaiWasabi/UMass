#!/usr/bin/perl
#-----------------------------------------
#Script Name: Regular expression
#Script Version: 1.0
#Date: 12-08-09
#Author: Tamar. Comments by AIK.
#Description: The script optimizes the range-separation parameter 
#omega in the range 100-800, as defined by the arguments with which the 
#subroutine 'Minimum' is called (see below). If you wish to
#optimize omega in a broader range, you need to edit this line.
#This script optimizes omega to satisfy two Koopmans conditions,
#both for IP and EA. Use OptOmegaIP.pl script to optimize for the IP 
#condition only. To execute the script, you need to create 3 inputs for a BNL 
#job using the same geometry and basis set for a neutral molecule (N.in), 
#anion (M.in) and cation (P.in) then type './OptOmegaIPEA.pl. 
#The script will run creating outputs for each step: M_*, etc. 
#Notes from Tamar: try to get from Q-Chem output file the convergence value:
#for this I look for regular expresion and than chop it. In this program I 
#read all the output file.
#Revision History: This is version No.2 - here I am referring to the simple 
#case of 1 run in each output or input file 
#-----------------------------------------

$jobid="oligomer";
$ncores=8;
$counter=0;
$optGamma=&Minimum(100,180,600);
print "gamma optimal:$optGamma\n";


####routines for finding minimum of a function #################


sub Minimum{
  $R=0.61803399;
  $Cr=1-$R;
  $tol=10**(-4);
  $a=$_[0];
  $b=$_[1];
  $c=$_[2];
  $X0=$a;
  $X3=$c;
  if (abs($c-$b)>abs($b-$a)){
    $X1=$b;
    $X2=$b+$Cr*($c-$b);
    }
  else{
    $X2=$b;
    $X1=$b-$Cr*($b-$a);}
  $f1=&GetFgamma($X1);
  $f2=&GetFgamma($X2);
  while(abs($X3-$X0) > $tol*(abs($X1)+abs($X2))){
    if ($f2 < $f1){
      $new=$R*$X2+$Cr*$X3;
      $Fnew=&GetFgamma($new);
      &ShiftThree($X0,$X1,$X2,$new);
      &ShiftTwo($f1,$f2,$Fnew); }
    else{
      $new=$R*$X1+$Cr*$X0;
      $Fnew=&GetFgamma($new);
      &ShiftThree($X3,$X2,$X1,$new);
      &ShiftTwo($f2,$f1,$Fnew);}
  }
      if($f1 < $f2){
      $Xmin=$X1;
      return $Xmin;}
    else{
      $Xmin=$X2;
      return $Xmin;}
  }



#this routine gets 4 num.
sub ShiftThree{
$_[0]=$_[1];
$_[1]=$_[2];
$_[2]=$_[3];}

#this routine gets 3 num. a,b,c 
sub ShiftTwo{
$_[0]=$_[1];
$_[1]=$_[2];}


####routines to get F(gamma)#################

#this routine uses all the other routine;it gets gamma value and return F(gamma) 
sub GetFgamma{
  $g=$_[0];
  $gamma=sprintf "%.0f" ,$g;
  print "$gamma\n";
  &Runfiles($gamma);
  $file1="P_$counter.out";
  $file2="M_$counter.out";
  $file3="N_$counter.out";
  $plus=&GetEnergies($file1);
  $minus=&GetEnergies($file2);
  $nuetral=&GetEnergies($file3);
  $S=&Mult($file3);
  if ($S){
    $Num=&NumAlphaOrb($file3); #checking what is the homo number in nuetral file,assume it is a singlet
    $HomoN=&GetAlphaOrb($file3,$Num); #getting the homo of nuetral
    $Num1=$Num+1;
    $LumoN=&GetAlphaOrb($file3,$Num1);}
  else{
    $NumAN=&NumAlphaOrb($file3); #checking the numbers of homo alpha and beta in minus
    $NumBN=&NumBetaOrb($file3);
    $HomoAN=&GetAlphaOrb($file3,$NumAN); #getting the energies of homo alpha and beta in Nuetral
    $HomoBN=&GetBetaOrb($file3,$NumBN);
    if ($HomoAN > $HomoBN){
      $HomoN=$HomoAN;}
    else {
      $HomoN=$HomoBN;}
    $Num1A=$NumAN+1;
    $Num1B=$NumBN+1;    
    $LumoNA=&GetAlphaOrb($file3,$Num1A);
    $LumoNB=&GetBetaOrb($file3,$Num1B);
    if ($LumoNA < $LumoNB){
      $LumoN=$LumoNA;}
    else {
      $LumoN=$LumoNB;}
  }
  $S=&Mult($file2);
    if ($S)
      {
        $NumA=&NumAlphaOrb($file2); #this is for a S
        $HomoM=&GetAlphaOrb($file2,$NumA); #getting the energies of homo alpha in Minus
      }
  else {
    $NumA=&NumAlphaOrb($file2); #checking the numbers of homo alpha and beta in minus
    $NumB=&NumBetaOrb($file2);
    $HomoMA=&GetAlphaOrb($file2,$NumA); #getting the energies of homo alpha and beta in Minus
    $HomoMB=&GetBetaOrb($file2,$NumB);
    if ($HomoMA > $HomoMB){
      $HomoM=$HomoMA;}
    else {
      $HomoM=$HomoMB;}
  }
  $F_gamma=Fgamma($plus,$minus,$nuetral,$HomoM,$HomoN); #Tunninig No2
  #$F_gamma=Fgamma($plus,$minus,$nuetral,$LumoN,$HomoN); #Tunninig No3
  #print "$F_gamma\n";
  #$F_gamma=Fea($minus,$nuetral,$HomoM);
 # $F_gamma=Fea($minus,$nuetral,$LumoN);
  return $F_gamma;
}


#this subroutine gets value of gamma and run 3 file: Neutral, Plus, and Minus.
sub Runfiles{
$counter++;
open(NewfileN,">N_$counter.in");
open(fileN,"N.in") || die("could not open N.in\n");
$string=<fileN>;
while ($string){
$string =~ s/omega\s+\d+/omega             $_[0]/;
print NewfileN "$string";
$string=<fileN>;}
close(fileN);
close(NewfileN);

open(NewfileM,">M_$counter.in");
open(fileM,"M.in") || die("could not open M.in\n");
$string=<fileM>;
while ($string){
$string =~ s/omega\s+\d+/omega           $_[0]/;
print NewfileM "$string";
$string=<fileM>;}
close(fileM);
close(NewfileM);

open(NewfileP,">P_$counter.in");
open(fileP,"P.in") || die("could not open P.in\n");
$string=<fileP>;
while ($string){
$string =~ s/omega\s+\d+/omega            $_[0]/;
print NewfileP "$string";
$string=<fileP>;}
close(fileP);
close(NewfileP);

if ($counter==1)
  {$result=`sed -i 's/scf_guess read/scf_guess sad/g' ?_1.in`;}
$result =`/home/zl53a/Q-Chem_5.3/development/bin/qchem -save -nt $ncores N_$counter.in N_$counter.out $jobid/N & /home/zl53a/Q-Chem_5.3/development/bin/qchem -save -nt $ncores P_$counter.in P_$counter.out $jobid/P & /home/zl53a/Q-Chem_5.3/development/bin/qchem -save -nt $ncores M_$counter.in M_$counter.out $jobid/M &`;
}



sub Omega{
  @temp=();
 open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($result = $string =~ /omega\s+\d+/){
      $data=$string;
      @temp=split(" ",$data);
    $gamma=$temp[1];}
    $string=<file>;}
  close(file);
  return $gamma;
}

#this subroutine gets a file and return the number of alpha orbitals
sub NumAlphaOrb{
  @temp=();
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($result = $string =~ /There are\s+\d+ alpha and\s+\d+ beta electrons/){
      $data=$string;
      @temp=split(" ",$data);
    $Num=$temp[2];}
    $string=<file>;}
  close(file);
  return $Num;
}


#this subroutine gets a file and returns the number of beta orbitals
sub NumBetaOrb{
  @temp=();
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($result = $string =~ /There are\s+\d+ alpha and\s+\d+ beta electrons/){
      $data=$string;
      @temp=split(" ",$data);
    $Num=$temp[5];}
    $string=<file>;}
  close(file);
  return $Num;
}

sub Mult{
  @temp=();
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($result = $string =~ /There are\s+\d+ alpha and\s+\d+ beta electrons/){
      $data=$string;
      @temp=split(" ",$data);
$beta=$temp[2];		
    $Alpha=$temp[5];}
    $string=<file>;}
$Num=$Alpha==$beta;
  close(file);
  return $Num;
}

#This subroutine get file name and return its energy
sub GetEnergies{
  @temp=();
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($result = $string =~ /.+Convergence criterion met/){
      $data=$string;
      @temp=split(" ",$data);
    $En=$temp[1];}
    $string=<file>;}
  close(file);
  return $En;}



# This subroutine gets file, orbital number and return its energy for alpha orbital
sub GetAlphaOrb{
  @tempOrb=();
  @OrbEn=();
  $alphaOrb=$_[1];
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($string =~ /Final Alpha MO Eigenvalues/){
      $string=<file>;
      until($result = $string =~ /\s+$alphaOrb\s+/){
        $string=<file>;}
      @OrbNum=split(" ",$string);
      $string=<file>;
      @OrbEn=split(" ",$string);
      $length=@OrbNum;}
      for ($i=0;$i<$length;$i++){
        if($OrbNum[$i]==$alphaOrb) {
          $OrbEnergy=$OrbEn[$i+1];}} #there is a displacement between the array of numvers and energies
    $string=<file>;}
  close(file);
  return $OrbEnergy;}




# This subroutine gets file,orbital number and return its energy for Beta  orbital
sub GetBetaOrb{
  @tempOrb=();
  @OrbEn=();
  $betaOrb=$_[1];
  open(file,$_[0]) || die("could not open $file\n");
  $string=<file>;
  while($string){
    if ($string =~ /Final Beta MO Eigenvalues/){
      $string=<file>;
      until($result = $string =~ /\s+$betaOrb\s+/){
        $string=<file>;}
      @OrbNum=split(" ",$string);
      $string=<file>;
      @OrbEn=split(" ",$string);
      $length=@OrbNum;}
      for ($i=0;$i<$length;$i++){
        if($OrbNum[$i]==$betaOrb) {
          $OrbEnergy=$OrbEn[$i+1];}} #there is a displacement between the array of numvers and energies
    $string=<file>;}
  close(file);
  return $OrbEnergy;}


#this routine gets energies plus minus nuetral Homominus,Homonuetral (in this order) and return  f(gamma)
sub Fgamma{
#this is what I need to get
$Plus=$_[0];
$Minus=$_[1];
$Nuetral=$_[2];
$HomoMinus=$_[3];
$HomoNuetral=$_[4];
########################
$IPscf=$Plus-$Nuetral;
$EAscf=$Nuetral-$Minus;
$diffEa=$EAscf+$HomoMinus;
$diffIP=$IPscf+$HomoNuetral;
$Fgamma=$diffEa**2+$diffIP**2;
return $Fgamma;
}


sub Fea{
#this is what I need to get
$Minus=$_[0];
$Nuetral=$_[1];
$HomoMinus=$_[2];
########################
$EAscf=$Nuetral-$Minus;
$diffEa=$EAscf+$HomoMinus;
$Fea=$diffEa**2;
return $Fea;
}
