import numpy as np
import matplotlib.pyplot as plt 

# Creamos los parámetros del resorte y la simulación
x = 1.0
p = 1.0
t = 0.0

m = 1.
k = 1.
omega = np.sqrt(k / m)

Tp = 2. * np.pi / omega
dt = Tp / 2000.

# Creamos los parámetros de la elipse
A = x
B = p / (omega * m)

# Creamos parámetros del ensamble microcanónico
E_min = 10.
E_max = 14.
N = 400

def x_el(t):
    return A * np.cos(omega * t) + B * np.sin(omega*t)

def p_el(t):
    return -A*omega*np.sin(omega*t) + B*omega*np.cos(omega*t)

# Creamos las evaluaciones del Hamiltoniano
def dHdx(x, p):
    return k * x

def dHdp(x, p):
    return p / m

# Creamos un integrador sencillo: Runge-Kutta 2
def integrator(x, p):
    
    # Creamos las primeras derivadas
    pdot = -dHdx(x, p)
    xdot = dHdp(x, p)
   
    # Aplicamos Runge-Kutta 2
    pk1 = pdot * dt
    xk1 = xdot * dt

    pk2 = dt * -dHdx(x + xk1/2., p + pk1/2.)
    xk2 = dt * dHdp(x + xk1/2., p + pk1/2.)
    
    # Actualizamos las variables
    x = x + xk2
    p = p + pk2

    # Retornamos
    return x, p

      
# Listas para guardar las elipses simuladas
t_list = list()
x_list = list()
p_list = list()

# Listas para guardar las elipses analíticas
x_el_list = list()
p_el_list = list()

# Corremos la simulación
for i in range(2000):
   t_list.append(t)
   x_list.append(x)
   p_list.append(p)
    
   x_el_list.append(x_el(t))
   p_el_list.append(p_el(t))

   t += dt 
   x, p = integrator(x ,p)


# Hacemos el plot del espacio de fase
plt.title("Espacio de fase: resorte")
plt.plot(x_list, p_list, label = "Simulación", lw = 4.0, c = "black")
plt.plot(x_el_list, p_el_list, label = "Analítico", alpha = 1.0, lw = 1.0, c = "red")
plt.grid()
plt.legend()
plt.xlabel("x")
plt.ylabel("p")
plt.show()



# ENSAMBLE MICROCANÓNICO

# Función para hallar la energía 
def E(x, p):
    return (p**2)/(2.*m) + 0.5*k*x**2

# Función para usar el método por rechazo
def CrearEnsamble():

    # Creamos los límites de un rectángulo que encierre la elipse
    x_lim = np.sqrt(2.0 * E_max / k)
    p_lim = np.sqrt(2.0 * E_max * m)

    # Rechazamos o aceptamos
    estados = list()            # Lista de estados iniciales válidos
    while len(estados) < N: 

        x0 = np.random.uniform(-x_lim, x_lim)
        p0 = np.random.uniform(-p_lim, p_lim)

        E0 = E(x0, p0)

        if E0 < E_max and E0 > E_min: 
            estados.append((x0, p0))

    return estados

# Creamos el ensamble
ensamble = np.array(CrearEnsamble())

# Graficamos el ensamble
plt.scatter(ensamble[::, 0], ensamble[::,1], c = np.random.uniform(0.0, 1.0, N), s = 3.0)
plt.grid()
plt.title("Ensamble microcanónico")
plt.xlabel("x")
plt.ylabel("p")
plt.show()
