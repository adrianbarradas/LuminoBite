with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Default showInspector to false
old_state = 'const [showInspector, setShowInspector] = useState(true);'
new_state = 'const [showInspector, setShowInspector] = useState(false);'
if old_state in text:
    text = text.replace(old_state, new_state, 1)
    print('Updated showInspector default to false')
else:
    print('ERROR: old_state not found')

# 2. Fix Header so it does not collapse or overlap (gap-3, shrink-0, min-w-0, responsive, clean flex wrap handling)
p1 = text.find('<header className="h-16 bg-lumino-dark')
p2 = text.find('</header>', p1) + len('</header>')

if p1 != -1 and p2 != -1:
    print('Found header to replace!')
    new_header = '''<header className="min-h-16 bg-lumino-dark text-white px-4 py-2 flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 shrink-0 z-50">
                        {/* Identidad de Marca */}
                        <div className="flex items-center gap-3 shrink-0">
                            <div className="font-montserrat font-black text-lg tracking-tighter flex items-center gap-2">
                                <div className="w-7 h-7 bg-lumino-pink rounded-full relative overflow-hidden flex items-center justify-center shadow-md shrink-0">
                                    <div className="w-3 h-3 bg-white rounded-full" />
                                </div>
                                <span className="tracking-tight">LUMINOBITE</span>
                                <span className="text-lumino-teal font-extrabold">CANVAS</span>
                                <span className="hidden xl:inline-block text-[10px] font-montserrat uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-slate-800 text-lumino-beige border border-slate-700">
                                    Food Science BI Studio
                                </span>
                            </div>

                            {/* Selector Rápido de Plantillas de Lienzo */}
                            {!presentationMode && (
                                <div className="hidden lg:flex items-center gap-1.5 ml-2 bg-slate-900/90 p-1 rounded-xl border border-slate-800 shrink-0">
                                    <button
                                        onClick={() => applyLayoutPreset('random')}
                                        title="Genera un tema de lienzo aleatorio con combinaciones profesionales"
                                        className="px-2.5 py-1.5 rounded-lg text-[11px] font-montserrat font-bold text-white bg-gradient-to-r from-teal-500 to-indigo-600 hover:from-teal-600 hover:to-indigo-700 shadow-sm flex items-center gap-1 transition"
                                    >
                                        <span>🎲</span> Tema Aleatorio
                                    </button>
                                    <button
                                        onClick={() => applyLayoutPreset('default')}
                                        className="px-2 py-1.5 rounded-lg text-[11px] font-montserrat font-bold text-slate-300 hover:bg-lumino-teal hover:text-white transition"
                                    >
                                        Vista General BI
                                    </button>
                                    <button
                                        onClick={() => applyLayoutPreset('allergen_focus')}
                                        className="px-2 py-1.5 rounded-lg text-[11px] font-montserrat font-bold text-slate-300 hover:bg-lumino-pink hover:text-white transition"
                                    >
                                        Alérgenos & Trazas
                                    </button>
                                    <button
                                        onClick={() => applyLayoutPreset('empty')}
                                        title="Vaciar completamente el lienzo para empezar de cero"
                                        className="px-2 py-1.5 rounded-lg text-[11px] font-montserrat font-bold text-rose-300 hover:bg-rose-900/60 transition"
                                    >
                                        🗑️ Vaciar
                                    </button>
                                </div>
                            )}
                        </div>

                        {/* Controles Centrales del Lienzo (Zoom, Cuadrícula, Filtro Activo) */}
                        <div className="flex items-center flex-wrap gap-2 shrink-0">
                            {currentSelectedBar && (
                                <div className="flex items-center gap-1.5 bg-lumino-teal/20 border border-lumino-teal px-2.5 py-1 rounded-full text-xs shrink-0">
                                    <span className="font-montserrat font-bold text-teal-300">
                                        🔍 <strong className="text-white uppercase">{currentSelectedBar.name}</strong>
                                    </span>
                                    <button 
                                        onClick={() => { setSelectedBarId(null); setHighlightedBarId(null); }}
                                        className="text-xs bg-lumino-teal text-white rounded-full w-4 h-4 flex items-center justify-center font-bold hover:bg-teal-700 ml-0.5"
                                        title="Quitar foco de la barra"
                                    >
                                        ×
                                    </button>
                                </div>
                            )}
                            <button
                                onClick={() => setFilters(prev => ({ ...prev, hideUnmatched: !prev.hideUnmatched }))}
                                className={`px-2.5 py-1.5 rounded-xl font-montserrat font-bold text-xs uppercase tracking-wider border transition flex items-center gap-1.5 shrink-0 ${
                                    filters.hideUnmatched
                                        ? 'bg-lumino-teal text-white border-teal-400 shadow-md'
                                        : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                                }`}
                                title="Reacomoda automáticamente el lienzo para mostrar solo barras e iconos aplicables según los filtros"
                            >
                                <span className={`w-2 h-2 rounded-full ${filters.hideUnmatched ? 'bg-white' : 'bg-slate-500'}`} />
                                <span className="hidden md:inline">{filters.hideUnmatched ? 'Reacomodo Auto (ON)' : 'Solo Filtradas'}</span>
                                <span className="md:hidden">Auto</span>
                            </button>
                            {activeStickerTag && (
                                <div className="flex items-center gap-1.5 bg-lumino-pink/20 border border-lumino-pink px-2.5 py-1 rounded-full text-xs shrink-0">
                                    <span className="font-montserrat font-bold text-pink-300">
                                        ✨ <strong className="text-white uppercase">{activeStickerTag}</strong>
                                    </span>
                                    <button 
                                        onClick={() => setActiveStickerTag(null)}
                                        className="text-xs bg-lumino-pink text-white rounded-full w-4 h-4 flex items-center justify-center font-bold ml-0.5"
                                    >
                                        ×
                                    </button>
                                </div>
                            )}

                            <div className="hidden md:flex items-center bg-slate-900 rounded-xl p-1 border border-slate-800 text-xs shrink-0">
                                <button
                                    onClick={() => setZoom(z => Math.max(0.55, +(z - 0.08).toFixed(2)))}
                                    className="px-2 py-0.5 hover:bg-slate-800 rounded-lg font-bold"
                                >
                                    −
                                </button>
                                <span className="px-2 font-roboto font-bold text-slate-300">
                                    {Math.round(zoom * 100)}%
                                </span>
                                <button
                                    onClick={() => setZoom(z => Math.min(1.35, +(z + 0.08).toFixed(2)))}
                                    className="px-2 py-0.5 hover:bg-slate-800 rounded-lg font-bold"
                                >
                                    +
                                </button>
                            </div>

                            <button
                                onClick={() => setGridStyle(g => g === 'dots' ? 'lines' : g === 'lines' ? 'clean' : 'dots')}
                                className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-montserrat font-bold text-slate-200 transition shrink-0"
                            >
                                {gridStyle === 'dots' ? 'Puntos' : gridStyle === 'lines' ? 'Líneas' : 'Limpio'}
                            </button>

                            {/* Selector de Tamaño de Cuadrícula */}
                            <div className="hidden xl:flex items-center bg-slate-900 rounded-xl px-2 py-1 border border-slate-800 text-xs gap-1 shrink-0">
                               <span className="text-[10px] font-montserrat font-bold text-slate-400 uppercase">Paso:</span>
                                {[16, 20, 24, 32, 48].map(size => (
                                    <button
                                        key={size}
                                        onClick={() => setGridSize(size)}
                                    className={`px-2 py-0.5 rounded text-[10.5px] font-roboto font-bold transition ${gridSize === size ? 'bg-lumino-teal text-white shadow-sm' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
                                    >
                                        {size}px
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Acciones de Exportación y Modo Presentación */}
                        <div className="flex items-center gap-2 shrink-0">
                            <button
                                onClick={() => setShowInspector(!showInspector)}
                                className={`px-3 py-1.5 rounded-xl font-montserrat font-bold text-xs uppercase tracking-wider border transition flex items-center gap-1.5 shrink-0 ${
                                    showInspector
                                        ? 'bg-lumino-teal text-white border-teal-400 shadow-md'
                                        : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                                }`}
                                title="Abrir o Cerrar el Inspector de Propiedades y Colores"
                            >
                                <span>⚙️ Inspector</span>
                                {selectedUid && <span className="w-2 h-2 rounded-full bg-lumino-pink animate-ping" />}
                            </button>

                            <button
                                onClick={() => setPresentationMode(!presentationMode)}
                                className={`hidden sm:inline-flex px-3 py-1.5 rounded-xl font-montserrat font-bold text-xs uppercase tracking-wider border transition shrink-0 ${
                                    presentationMode
                                        ? 'bg-amber-400 text-lumino-dark border-amber-300'
                                        : 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
                                }`}
                            >
                                {presentationMode ? 'Salir Presentación' : 'Presentación'}
                            </button>

                            <button
                                onClick={handleExportJSON}
                                className="hidden lg:inline-flex px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-montserrat font-bold text-xs uppercase tracking-wider transition shadow shrink-0"
                                title="Guardar diseño en formato JSON"
                            >
                                JSON
                            </button>

                            <button
                                onClick={handleExportPNG}
                                disabled={isExporting}
                                className="px-3.5 py-1.5 rounded-xl bg-lumino-pink hover:bg-pink-600 text-white font-montserrat font-extrabold text-xs uppercase tracking-wider transition shadow-lg flex items-center gap-1.5 shrink-0"
                            >
                                <span>📷 Exportar PNG</span>
                            </button>
                        </div>
                    </header>'''
    text = text[:p1] + new_header + text[p2:]
    print('Replaced header successfully!')
else:
    print('ERROR: header boundaries not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Saved index.html!')

