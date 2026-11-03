with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Brand area in Header with SaaS Tier badge & Dataset Status
old_brand_end = '''                                <span className="hidden xl:inline-block text-[10px] font-montserrat uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-slate-800 text-lumino-beige border border-slate-700">
                                    Food Science BI Studio
                                </span>'''

new_brand_end = '''                                <span className="hidden xl:inline-block text-[10px] font-montserrat uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-slate-800 text-lumino-beige border border-slate-700">
                                    Food Science BI Studio
                                </span>
                                {/* Badge de Suscripción SaaS (Trial / Pro / Enterprise) */}
                                <button
                                    onClick={() => setShowPricingModal(true)}
                                    className="px-2.5 py-0.5 rounded-full text-[10px] font-montserrat font-extrabold uppercase tracking-wider bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 shadow-sm hover:scale-105 transition flex items-center gap-1 cursor-pointer"
                                    title="Ver planes de suscripción mensual/anual para equipos de I+D"
                                >
                                    <span>💎</span>
                                    <span>Plan {userTier.toUpperCase()}</span>
                                </button>'''

if old_brand_end in text:
    text = text.replace(old_brand_end, new_brand_end, 1)
    print('Updated brand header with SaaS Tier button!')
else:
    print('ERROR: old_brand_end not found')

# 2. Add "Subir Datos (CSV/Excel)" Button and Dataset state pill in Header right actions
old_export_btn = '''                            <button
                                onClick={handleExportPNG}'''

new_upload_btn = '''                            {/* Botón de Ingestión Libre de Datos SaaS (Excel / CSV) */}
                            <button
                                onClick={() => setShowUploadModal(true)}
                                className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-teal-500 to-indigo-600 hover:from-teal-600 hover:to-indigo-700 text-white font-montserrat font-bold text-xs uppercase tracking-wider transition shadow-md flex items-center gap-1.5 shrink-0"
                                title="Sube archivos CSV o Excel en cualquier formato. El motor inteligente los normalizará automáticamente."
                            >
                                <span>📁 Subir Datos</span>
                                {datasetInfo && <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />}
                            </button>

                            <button
                                onClick={handleExportPNG}'''

if old_export_btn in text:
    text = text.replace(old_export_btn, new_upload_btn, 1)
    print('Added Subir Datos button in header!')
else:
    print('ERROR: old_export_btn not found')

# 3. Add Dataset Status Pill in Header center if custom dataset is active
old_center_controls = '''                        {/* Controles Centrales del Lienzo (Zoom, Cuadrícula, Filtro Activo) */}
                        <div className="flex items-center flex-wrap gap-2 shrink-0">'''

new_center_controls = '''                        {/* Controles Centrales del Lienzo (Zoom, Cuadrícula, Filtro Activo) */}
                        <div className="flex items-center flex-wrap gap-2 shrink-0">
                            {datasetInfo && (
                                <div className="flex items-center gap-2 bg-indigo-950/70 border border-indigo-500/50 px-2.5 py-1 rounded-full text-xs shrink-0">
                                    <span className="font-montserrat font-bold text-indigo-300">
                                        📊 Dataset: <strong className="text-white">{datasetInfo.fileName}</strong> ({datasetInfo.importedCount} fórmulas)
                                    </span>
                                    <button
                                        onClick={restoreBenchmarkDataset}
                                        className="text-[10px] text-slate-400 hover:text-white px-1.5 py-0.5 rounded bg-slate-800 transition"
                                        title="Volver al benchmark base oficial"
                                    >
                                        Restablecer
                                    </button>
                                </div>
                            )}'''

if old_center_controls in text:
    text = text.replace(old_center_controls, new_center_controls, 1)
    print('Added Dataset Status Pill in header center!')
else:
    print('ERROR: old_center_controls not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated index.html part 2!')

