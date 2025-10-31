import React, { useState, useEffect, FC, ReactNode } from 'react';

// --- Definición de Componentes Auxiliares ---
// Se definen fuera del componente principal para evitar re-renderizados innecesarios.

// Icono genérico para la barra lateral
const NavIcon: FC<{ children: ReactNode }> = ({ children }) => (
  <span className="mr-3">{children}</span>
);

// Enlace de navegación en la barra lateral
interface NavLinkProps {
  label: string;
  viewName: string;
  activeView: string;
  setActiveView: (view: string) => void;
  children: ReactNode;
}

const NavLink: FC<NavLinkProps> = ({ label, viewName, activeView, setActiveView, children }) => {
  const isActive = activeView === viewName;
  const baseClasses = "flex items-center px-4 py-2 mt-2 text-gray-300 transition-colors duration-200 transform rounded-md hover:bg-gray-700 hover:text-white";
  const activeClasses = "bg-gray-700 text-white";

  return (
    <a
      href="#"
      className={`${baseClasses} ${isActive ? activeClasses : ''}`}
      onClick={(e) => {
        e.preventDefault();
        setActiveView(viewName);
      }}
    >
      {children}
      <span className="mx-4 font-medium">{label}</span>
    </a>
  );
};


// Tarjeta para mostrar métricas clave
interface StatCardProps {
  title: string;
  value: string;
  description: string;
}
const StatCard: FC<StatCardProps> = ({ title, value, description }) => (
  <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
    <h3 className="text-lg font-semibold text-gray-600 mb-2">{title}</h3>
    <p className="text-4xl font-bold text-gray-900">{value}</p>
    <p className="text-sm text-gray-500 mt-1">{description}</p>
    {/* COMENTARIO: Aquí se podría llamar a una función para obtener datos específicos para esta tarjeta. */}
  </div>
);


// Contenedor para visualizaciones como gráficos o tablas
interface ContentBoxProps {
    title: string;
    children: ReactNode;
}

const ContentBox: FC<ContentBoxProps> = ({ title, children }) => (
    <div className="mt-10 bg-white p-6 rounded-lg shadow-md">
        <h3 className="font-semibold text-xl mb-4 text-gray-700">{title}</h3>
        {children}
    </div>
);


// --- Componente Principal de la Aplicación ---

const App: FC = () => {
  const [activeView, setActiveView] = useState('inicio');

  // Simula la carga de datos cuando cambia la vista activa
  useEffect(() => {
    // COMENTARIO: Aquí es donde se realizaría la llamada a la función principal para cargar los datos de la vista.
    // Por ejemplo: `cargarDatosParaVista(activeView);`
    console.log(`Cargando datos para la vista: ${activeView}`);
    
    // La siguiente línea es para deshabilitar la advertencia de 'exhaustive-deps' de ESLint.
    // Es seguro en este caso porque solo queremos que se ejecute cuando 'activeView' cambia.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeView]);

  const renderContent = () => {
    // COMENTARIO: El contenido se renderiza condicionalmente basado en la vista activa.
    // Cada caso podría ser un componente más complejo en un archivo separado.
    switch(activeView) {
        case 'inicio':
            return (
                <div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {/* COMENTARIO: Los datos para estas tarjetas vendrían de una llamada a una API */}
                        <StatCard title="Ventas Totales" value="€12,345" description="Mes actual" />
                        <StatCard title="Nuevos Usuarios" value="89" description="+15% vs mes anterior" />
                        <StatCard title="Tasa de Rebote" value="23.4%" description="-2% vs mes anterior" />
                        <StatCard title="Satisfacción" value="95%" description="Basado en 250 encuestas" />
                    </div>

                    <ContentBox title="Gráfico de Tendencias de Ventas">
                        {/* COMENTARIO: Aquí se llamaría a un componente de gráficos (ej. Recharts, D3) */}
                        {/* y se le pasarían los datos cargados. */}
                        <div className="h-80 bg-gray-50 rounded flex items-center justify-center border border-dashed">
                            <p className="text-gray-400">[Contenedor para el gráfico de tendencias]</p>
                        </div>
                    </ContentBox>
                </div>
            );
        case 'analisis':
            return (
                <div>
                    <ContentBox title="Análisis Detallado de Datos">
                        {/* COMENTARIO: Aquí iría una función o componente que renderice una tabla interactiva. */}
                        <div className="h-96 bg-gray-50 rounded flex items-center justify-center border border-dashed">
                            <p className="text-gray-400">[Contenedor para la tabla de datos avanzada]</p>
                        </div>
                    </ContentBox>
                </div>
            );
        case 'reportes':
             return (
                <div>
                    <ContentBox title="Generador de Reportes">
                        {/* COMENTARIO: Aquí iría una función o componente para configurar y descargar reportes. */}
                        <div className="h-64 bg-gray-50 rounded flex flex-col items-center justify-center border border-dashed">
                           <p className="text-gray-400 mb-4">[Contenedor para opciones de reporte]</p>
                           <button className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                            Generar Reporte
                           </button>
                        </div>
                    </ContentBox>
                </div>
            );
        default:
            return <div>Vista no encontrada</div>;
    }
  }


  return (
    <div className="flex h-screen bg-gray-100 font-sans">
      {/* --- BARRA LATERAL (Sidebar) --- */}
      <aside className="hidden md:flex w-64 flex-col bg-gray-800 text-white p-4">
        <div className="flex items-center mb-8">
          <svg className="w-8 h-8 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          <h1 className="text-2xl font-bold">Dashboard</h1>
        </div>
        <nav className="flex-1">
          <NavLink label="Inicio" viewName="inicio" activeView={activeView} setActiveView={setActiveView}>
            <NavIcon>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
            </NavIcon>
          </NavLink>
          <NavLink label="Análisis" viewName="analisis" activeView={activeView} setActiveView={setActiveView}>
            <NavIcon>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </NavIcon>
          </NavLink>
          <NavLink label="Reportes" viewName="reportes" activeView={activeView} setActiveView={setActiveView}>
            <NavIcon>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </NavIcon>
          </NavLink>
        </nav>
      </aside>

      {/* --- CONTENIDO PRINCIPAL (Main Content) --- */}
      <main className="flex-1 p-6 sm:p-10 overflow-auto">
        <header className="mb-8">
          <h2 className="text-3xl font-semibold text-gray-800 capitalize">
            {activeView === 'inicio' ? 'Vista General' : activeView}
          </h2>
        </header>
        
        {renderContent()}

      </main>
    </div>
  );
};

export default App;
