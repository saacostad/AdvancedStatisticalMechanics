#include <iostream>
#include <cmath>
#include "Random64.h"
using namespace std;

const double kB=1;
const double J=1;

const int L=8;
const int L2=L*L;

class SpinSystem{
private:
  int s[L][L], E, M;
public:
  void Inicie(void);
  void UnPasoDeMetropolis(double Beta,Crandom & ran64);
  double GetE(void){return 1.0*E;};
  double GetM(void){return fabs(1.0*M);};
};
void SpinSystem::Inicie(void){
  for(int i=0;i<L;i++)
    for(int j=0;j<L;j++)
      s[i][j]=-1;
  E=-2*L2*J; M=-L2;
}
void SpinSystem::UnPasoDeMetropolis(double Beta,Crandom & ran64){
  int n,i,j,dE;
  //Escojo un espin al azar;
  n=(int) L2*ran64.r(); i=n/L; j=n%L;
  //Calculo el dE que tendría si lo volteo;
  dE=2*J*s[i][j]*(s[(i+1)%L][j]+s[(i+L-1)%L][j]+s[i][(j+1)%L]+s[i][(j+L-1)%L]);
  if(dE<=0)
    {s[i][j]*=(-1); E+=dE; M+=2*s[i][j];} //lo volteo;
  else
    if(ran64.r()<exp(-Beta*dE))
      {s[i][j]*=(-1); E+=dE; M+=2*s[i][j];} //lo volteo;
}

const int teq=600*pow(L/8.0,2.4); //mcss= Monte Carlo Steps per Site
const int tcorr=50*pow(L/8.0,2.4); //mcss= Monte Carlo Steps per Site
const int Nmuestras=10000;

int main(void){
  SpinSystem Ising2D;
  Crandom ran64(42);
  double T,Beta;
  int t,mcs,cmuestras;

  double E,sumE,sumE2; double M,sumM,sumM2,sumM4;
  double Eprom,E2prom,Mprom,M2prom,M4prom;
  double Cv,Xs,UBinder;

  for(T=0.8;T<=3.0;T+=0.1){
    Beta=1.0/(kB*T);
    
    Ising2D.Inicie();
    //Llegar a la distribucion limite de equilibrio
    for(t=0;t<teq;t++)
      for(mcs=0;mcs<L2;mcs++)
	Ising2D.UnPasoDeMetropolis(Beta,ran64);
    
    //Tomar Muestras
    sumE=sumE2=sumM=sumM2=sumM4=0;
    for(cmuestras=0;cmuestras<Nmuestras;cmuestras++){
      //Se miden los valores
      E=Ising2D.GetE();   M=Ising2D.GetM();
      //Se acumulan
      sumE+=E; sumE2+=E*E; sumM+=M; sumM2+=M*M; sumM4+=M*M*M*M;
      //Se va a la siguiente muestra
      for(t=0;t<tcorr;t++)
	for(mcs=0;mcs<L2;mcs++)
	  Ising2D.UnPasoDeMetropolis(Beta,ran64);
    }
    
    //Procesar los datos obtenidos
    Eprom=sumE/Nmuestras;  E2prom=sumE2/Nmuestras; 
    Mprom=sumM/Nmuestras;  M2prom=sumM2/Nmuestras;   M4prom=sumM4/Nmuestras;
    //Construyo las variables de salida
    Cv=(1.0/(kB*T*T))*(E2prom-Eprom*Eprom);
    Xs=(1.0/(kB*T))*(M2prom-Mprom*Mprom);
    UBinder=1.0-1.0/3.0*M4prom/(M2prom*M2prom);
    //Imprimo
    cout<<T<<" "<<Eprom<<" "<<Mprom<<" "<<Cv<<" "<<Xs<<" "<<UBinder<<endl;
  }
  return 0;
}

