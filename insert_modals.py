with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                        {showInspector && !presentationMode && !focusedBarId && (
                            <PropertyInspectorSidebar
                                selectedItem={items.find(i => i.uid === selectedUid)}
                                onUpdateProps={updateSelectedItemProps}
                                onClose={() => setShowInspector(false)}
                                allBars={activeBarsData}
                                allIcons={CUTE_STICKERS_LIBRARY}
                                onDelete={deleteSelectedItem}
                                onDuplicate={duplicateSelectedItem}
                                onFocusBar={(bId) => setFocusedBarId(bId)}
                            />
                        )}
                    </div>
                </div>'''

replacement = '''                        {showInspector && !presentationMode && !focusedBarId && (
                            <PropertyInspectorSidebar
                                selectedItem={items.find(i => i.uid === selectedUid)}
                                onUpdateProps={updateSelectedItemProps}
                                onClose={() => setShowInspector(false)}
                                allBars={activeBarsData}
                                allIcons={CUTE_STICKERS_LIBRARY}
                                onDelete={deleteSelectedItem}
                                onDuplicate={duplicateSelectedItem}
                                onFocusBar={(bId) => setFocusedBarId(bId)}
                            />
                        )}
                    </div>

                    {/* ==================================================================== */}
                    {/* MODAL 1: MOTOR DE SUBIDA LIBRE DE ARCHIVOS (EXCEL / CSV ZERO-TEMPLATE)  */}
                    {/* ==================================================================== */}
                    {showUploadModal && (
                        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/75 backdrop-blur-md animate-fadeIn">
                            <div className="bg-white rounded-3xl max-w-xl w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
                                <div className="p-6 bg-slate-900 text-white flex items-start justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-teal-500 to-indigo-600 flex items-center justify-center text-xl shadow">
                                            📁
                                        </div>
                                        <div>
                                            <h3 className="font-montserrat font-black text-lg tracking-tight">
                                                Cargar Datos de I+D (Zero-Template)
                                            </h3>
                                            <p className="text-xs text-slate-300 font-sans mt-0.5">
                                                Sube tus tablas en el formato que tengas. Normalización e inferencia automática.
                                            </p>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => setShowUploadModal(false)}
                                        className="text-slate-400 hover:text-white text-xl p-1 font-bold"
                                    >
                                        ✕
                                    </button>
                                </div>

                                <div className="p-6 space-y-5">
                                    {/* Zona de Drop / Input de Archivo */}
                                    <div
                                        onClick={() => datasetFileInputRef.current?.click()}
                                        className="border-2 border-dashed border-teal-500/50 hover:border-teal-500 bg-teal-50/40 hover:bg-teal-50/80 rounded-2xl p-8 text-center cursor-pointer transition flex flex-col items-center justify-center group"
                                    >
                                        <input
                                            ref={datasetFileInputRef}
                                            type="file"
                                            accept=".csv, .xlsx, .xls, text/csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                                            onChange={handleFileUpload}
                                            className="hidden"
                                        />
                                        <div className="w-16 h-16 rounded-full bg-white shadow-md flex items-center justify-center text-3xl mb-3 group-hover:scale-110 transition">
                                            📊
                                        </div>
                                        <div className="font-montserrat font-extrabold text-sm text-lumino-dark">
                                            {isProcessingFile ? 'Procesando archivo con IA heurística...' : 'Haz clic o arrastra tu archivo Excel o CSV aquí'}
                                        </div>
                                        <p className="text-xs text-slate-500 mt-1 max-w-sm">
                                            Acepta archivos <strong>.xlsx</strong>, <strong>.xls</strong> o <strong>.csv</strong> con cualquier orden de columnas o nombres de encabezado.
                                        </p>
                                        <div className="mt-3 flex items-center gap-2">
                                            <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-600 shadow-xs">
                                                ✓ Sin plantillas rígidas
                                            </span>
                                            <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-600 shadow-xs">
                                                ✓ Inferencia de Alérgenos
                                            </span>
                                            <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-white border border-slate-200 text-slate-600 shadow-xs">
                                                ✓ Generación de Lienzo Auto
                                            </span>
                                        </div>
                                    </div>

                                    {/* Mensaje de Error en Ingestión */}
                                    {uploadError && (
                                        <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-xs flex items-center gap-2">
                                            <span>⚠️</span>
                                            <span>{uploadError}</span>
                                        </div>
                                    )}

                                    {/* Dataset Activo Actual (si existe) */}
                                    {datasetInfo && (
                                        <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-2xl flex items-center justify-between">
                                            <div>
                                                <div className="text-[11px] font-montserrat font-bold text-slate-700 flex items-center gap-1.5">
                                                    <span className="w-2 h-2 rounded-full bg-emerald-500" />
                                                    Dataset Activo: {datasetInfo.fileName}
                                                </div>
                                                <div className="text-[10px] text-slate-500 mt-0.5">
                                                    {datasetInfo.importedCount} fórmulas procesadas • {datasetInfo.headers.length} columnas detectadas
                                                </div>
                                            </div>
                                            <button
                                                onClick={() => {
                                                    restoreBenchmarkDataset();
                                                    setShowUploadModal(false);
                                                }}
                                                className="px-2.5 py-1 rounded-lg text-[10px] font-bold text-rose-600 hover:bg-rose-100 transition border border-rose-200"
                                            >
                                                Restablecer a Benchmark
                                            </button>
                                        </div>
                                    )}

                                    {/* Explicación de Valor SaaS */}
                                    <div className="text-[11px] text-slate-500 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100">
                                        💡 <strong>¿Cómo funciona el motor Zero-Template?</strong> Puedes exportar datos directo desde tu LIMS, software de laboratorio o Excel interno. Nuestro algoritmo reconoce sinónimos de ingredientes, calorías, macronutrientes, alérgenos y oligoelementos, calculando carbos netos y generando visualizaciones aleatorias pero adaptadas a tus datos.
                                    </div>
                                </div>

                                <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-end">
                                    <button
                                        onClick={() => setShowUploadModal(false)}
                                        className="px-4 py-2 rounded-xl text-xs font-montserrat font-bold text-slate-700 hover:bg-slate-200 transition"
                                    >
                                        Cerrar
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* ==================================================================== */}
                    {/* MODAL 2: PLANES DE SUSCRIPCIÓN SAAS PARA EQUIPOS DE I+D             */}
                    {/* ==================================================================== */}
                    {showPricingModal && (
                        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
                            <div className="bg-white rounded-3xl max-w-4xl w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
                                <div className="p-6 bg-lumino-dark text-white flex items-center justify-between shrink-0">
                                    <div>
                                        <div className="flex items-center gap-2">
                                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-montserrat font-black bg-lumino-pink text-white uppercase tracking-wider">
                                                Plataforma SaaS I+D
                                            </span>
                                            <span className="text-xs text-slate-400">Nutritional BI & Canvas Intelligence</span>
                                        </div>
                                        <h2 className="font-montserrat font-black text-2xl tracking-tight mt-1">
                                            Planes de Suscripción para Equipos Científicos
                                        </h2>
                                        <p className="text-xs text-slate-300 font-sans mt-0.5">
                                            Acceso total para subir tus fórmulas, auditar ingredientes y generar tableros ejecutivos interactivos.
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => setShowPricingModal(false)}
                                        className="text-slate-400 hover:text-white text-2xl p-1 font-bold"
                                    >
                                        ✕
                                    </button>
                                </div>

                                <div className="p-6 overflow-y-auto space-y-6">
                                    {/* Selector de Ciclo (Mensual vs Anual con descuento) */}
                                    <div className="flex items-center justify-center">
                                        <div className="bg-slate-100 p-1 rounded-2xl flex items-center gap-1 border border-slate-200">
                                            <button
                                                onClick={() => setSubscriptionCycle('monthly')}
                                                className={`px-4 py-1.5 rounded-xl text-xs font-montserrat font-bold transition ${
                                                    subscriptionCycle === 'monthly' ? 'bg-lumino-dark text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                                }`}
                                            >
                                                Facturación Mensual
                                            </button>
                                            <button
                                                onClick={() => setSubscriptionCycle('annual')}
                                                className={`px-4 py-1.5 rounded-xl text-xs font-montserrat font-bold transition flex items-center gap-1.5 ${
                                                    subscriptionCycle === 'annual' ? 'bg-gradient-to-r from-teal-500 to-indigo-600 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                                }`}
                                            >
                                                <span>Facturación Anual</span>
                                                <span className="bg-amber-400 text-slate-950 text-[9px] font-black px-1.5 py-0.2 rounded-full uppercase">
                                                    -20% OFF
                                                </span>
                                            </button>
                                        </div>
                                    </div>

                                    {/* Grid de 3 Niveles SaaS: Starter Trial, Team Pro, Enterprise Suite */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                                        {/* PLAN 1: TRIAL */}
                                        <div className={`rounded-3xl p-5 border flex flex-col justify-between transition ${
                                            userTier === 'trial' ? 'border-teal-500 ring-2 ring-teal-500 bg-teal-50/20' : 'border-slate-200 bg-white hover:border-slate-300'
                                        }`}>
                                            <div>
                                                <div className="flex items-center justify-between">
                                                    <h3 className="font-montserrat font-black text-sm text-lumino-dark">TRIAL LAB</h3>
                                                    {userTier === 'trial' && <span className="text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-teal-100 text-teal-800">Plan Actual</span>}
                                                </div>
                                                <div className="mt-3">
                                                    <span className="font-montserrat font-black text-3xl text-lumino-dark">$0</span>
                                                    <span className="text-xs text-slate-400 font-sans"> / 14 días</span>
                                                </div>
                                                <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                                                    Para investigadores individuales que desean validar modelos con el benchmark oficial.
                                                </p>
                                                <ul className="mt-4 space-y-2 text-xs text-slate-600 font-medium border-t pt-3">
                                                    <li className="flex items-center gap-2">✓ Benchmark de 5 marcas globales</li>
                                                    <li className="flex items-center gap-2">✓ Filtros biotecnológicos en vivo</li>
                                                    <li className="flex items-center gap-2">✓ 1 archivo CSV personalizado de prueba</li>
                                                    <li className="flex items-center gap-2 text-slate-400">✕ Sin exportación vectorizada PNG Ultra</li>
                                                </ul>
                                            </div>
                                            <button
                                                onClick={() => {
                                                    setUserTier('trial');
                                                    setShowPricingModal(false);
                                                }}
                                                className={`mt-6 w-full py-2.5 rounded-xl font-montserrat font-bold text-xs uppercase tracking-wider transition ${
                                                    userTier === 'trial' ? 'bg-slate-200 text-slate-700' : 'bg-slate-100 hover:bg-slate-200 text-slate-800'
                                                }`}
                                            >
                                                {userTier === 'trial' ? 'Activo' : 'Seleccionar Trial'}
                                            </button>
                                        </div>

                                        {/* PLAN 2: PRO I+D (Recomendado) */}
                                        <div className={`rounded-3xl p-6 border-2 flex flex-col justify-between relative shadow-xl transition ${
                                            userTier === 'pro' ? 'border-lumino-teal ring-2 ring-teal-500 bg-white' : 'border-teal-500 bg-white'
                                        }`}>
                                            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-teal-500 to-indigo-600 text-white font-montserrat font-black text-[9px] uppercase tracking-widest px-3 py-1 rounded-full shadow-md">
                                                RECOMENDADO PARA I+D
                                            </div>
                                            <div>
                                                <div className="flex items-center justify-between">
                                                    <h3 className="font-montserrat font-black text-base text-lumino-dark">TEAM PRO I+D</h3>
                                                    {userTier === 'pro' && <span className="text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-teal-100 text-teal-800">Plan Actual</span>}
                                                </div>
                                                <div className="mt-3">
                                                    <span className="font-montserrat font-black text-3xl text-lumino-dark">
                                                        ${subscriptionCycle === 'annual' ? '79' : '99'}
                                                    </span>
                                                    <span className="text-xs text-slate-400 font-sans"> / usuario / mes</span>
                                                    {subscriptionCycle === 'annual' && (
                                                        <div className="text-[10px] text-teal-600 font-bold mt-0.5">Facturado anualmente ($948/año)</div>
                                                    )}
                                                </div>
                                                <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                                                    Acceso sin límites para equipos de formulación de alimentos que suben datasets propios.
                                                </p>
                                                <ul className="mt-4 space-y-2 text-xs text-slate-600 font-medium border-t pt-3">
                                                    <li className="flex items-center gap-2">✓ <strong>Ingestión Ilimitada</strong> Excel y CSV</li>
                                                    <li className="flex items-center gap-2">✓ Inferencia Heurística Zero-Template</li>
                                                    <li className="flex items-center gap-2">✓ Visualizaciones y dashboards auto-generados</li>
                                                    <li className="flex items-center gap-2">✓ Inspector de marcas, logos, texturas y fades</li>
                                                    <li className="flex items-center gap-2">✓ Exportación PNG Ultra HD & JSON ilimitada</li>
                                                </ul>
                                            </div>
                                            <button
                                                onClick={() => {
                                                    setUserTier('pro');
                                                    setShowPricingModal(false);
                                                }}
                                                className="mt-6 w-full py-2.5 rounded-xl font-montserrat font-black text-xs uppercase tracking-wider bg-lumino-teal hover:bg-teal-700 text-white shadow-md transition hover:scale-[1.02]"
                                            >
                                                {userTier === 'pro' ? 'Plan Activo' : 'Comenzar Suscripción Pro'}
                                            </button>
                                        </div>

                                        {/* PLAN 3: ENTERPRISE */}
                                        <div className={`rounded-3xl p-5 border flex flex-col justify-between transition ${
                                            userTier === 'enterprise' ? 'border-amber-400 ring-2 ring-amber-400 bg-amber-50/20' : 'border-slate-200 bg-white hover:border-slate-300'
                                        }`}>
                                            <div>
                                                <div className="flex items-center justify-between">
                                                    <h3 className="font-montserrat font-black text-sm text-lumino-dark">ENTERPRISE</h3>
                                                    {userTier === 'enterprise' && <span className="text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-100 text-amber-800">Plan Actual</span>}
                                                </div>
                                                <div className="mt-3">
                                                    <span className="font-montserrat font-black text-3xl text-lumino-dark">
                                                        ${subscriptionCycle === 'annual' ? '249' : '299'}
                                                    </span>
                                                    <span className="text-xs text-slate-400 font-sans"> / mes (equipo completo)</span>
                                                </div>
                                                <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                                                    Para plantas productoras multinacionales y laboratorios con múltiples líneas de producto.
                                                </p>
                                                <ul className="mt-4 space-y-2 text-xs text-slate-600 font-medium border-t pt-3">
                                                    <li className="flex items-center gap-2">✓ Todo lo incluido en Pro I+D</li>
                                                    <li className="flex items-center gap-2">✓ Conexión API directa a ERP / LIMS</li>
                                                    <li className="flex items-center gap-2">✓ Auditoría multi-planta de alérgenos</li>
                                                    <li className="flex items-center gap-2">✓ Soporte bioinformático prioritario 24/7</li>
                                                </ul>
                                            </div>
                                            <button
                                                onClick={() => {
                                                    setUserTier('enterprise');
                                                    setShowPricingModal(false);
                                                }}
                                                className={`mt-6 w-full py-2.5 rounded-xl font-montserrat font-bold text-xs uppercase tracking-wider transition ${
                                                    userTier === 'enterprise' ? 'bg-amber-400 text-slate-950 font-black' : 'bg-slate-900 hover:bg-slate-800 text-white'
                                                }`}
                                            >
                                                {userTier === 'enterprise' ? 'Plan Activo' : 'Contactar Enterprise'}
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                                    <div className="text-xs text-slate-400 flex items-center gap-1.5">
                                        <span>🔒 Pagos cifrados vía Stripe SaaS • Cancela en cualquier momento</span>
                                    </div>
                                    <button
                                        onClick={() => setShowPricingModal(false)}
                                        className="px-4 py-2 rounded-xl text-xs font-montserrat font-bold text-slate-700 hover:bg-slate-200 transition"
                                    >
                                        Continuar al Canvas
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>'''

if target in text:
    text = text.replace(target, replacement, 1)
    print('Inserted Modals successfully!')
else:
    print('ERROR: target for modals not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated index.html part 3!')

