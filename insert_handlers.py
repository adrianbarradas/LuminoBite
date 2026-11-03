with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find handleExportPNG definition inside App
p_png = text.find('const handleExportPNG =')
if p_png == -1:
    print('ERROR: handleExportPNG not found')
    exit()

saas_handlers = '''            // ========================================================================
            // MOTOR DE INGESTIÓN LIBRE DE DATOS (EXCEL / CSV) & NORMALIZACIÓN BI
            // ========================================================================
            const handleFileUpload = (e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                setIsProcessingFile(true);
                setUploadError(null);

                const fileName = file.name;
                const isExcel = fileName.endsWith('.xlsx') || fileName.endsWith('.xls');

                const processParsedRows = (rows) => {
                    try {
                        if (!rows || rows.length === 0) {
                            throw new Error('El archivo no contiene filas o datos tabulares legibles.');
                        }
                        if (!window.LuminoDatasetEngine) {
                            throw new Error('Motor de inferencia heurística no disponible.');
                        }
                        const normalized = window.LuminoDatasetEngine.normalizeRows(rows);
                        if (normalized.length === 0) {
                            throw new Error('No se pudieron inferir métricas o productos del archivo.');
                        }
                        setCustomBars(normalized);
                        setDatasetInfo({
                            fileName,
                            totalRows: rows.length,
                            importedCount: normalized.length,
                            importedAt: new Date().toLocaleTimeString(),
                            headers: Object.keys(rows[0] || {})
                        });

                        // Genera automáticamente un Lienzo con distribución y modelos adaptados
                        const autoCanvasItems = window.LuminoDatasetEngine.generateDatasetCanvas(
                            normalized,
                            `AUDITORÍA BI: ${fileName.replace(/\.[^/.]+$/, '').toUpperCase()}`
                        );
                        setItems(autoCanvasItems);
                        resetFilters();
                        setIsProcessingFile(false);
                        setShowUploadModal(false);
                        setExportNotice(`¡Dataset procesado con éxito! Se generó una visualización personalizada para ${normalized.length} fórmulas.`);
                        setTimeout(() => setExportNotice(null), 4000);
                    } catch (err) {
                        setIsProcessingFile(false);
                        setUploadError(err.message || 'Error procesando el archivo de datos.');
                    }
                };

                if (isExcel) {
                    const reader = new FileReader();
                    reader.onload = (evt) => {
                        try {
                            const data = new Uint8Array(evt.target.result);
                            const workbook = XLSX.read(data, { type: 'array' });
                            const firstSheetName = workbook.SheetNames[0];
                            const worksheet = workbook.Sheets[firstSheetName];
                            const jsonRows = XLSX.utils.sheet_to_json(worksheet, { defval: '' });
                            processParsedRows(jsonRows);
                        } catch (err) {
                            setIsProcessingFile(false);
                            setUploadError('Error al leer el archivo Excel: ' + err.message);
                        }
                    };
                    reader.readAsArrayBuffer(file);
                } else {
                    // CSV parse con PapaParse (auto-detecta delimitador comas, puntos y coma, tabs)
                    Papa.parse(file, {
                        header: true,
                        skipEmptyLines: true,
                        dynamicTyping: true,
                        complete: (results) => {
                            processParsedRows(results.data);
                        },
                        error: (err) => {
                            setIsProcessingFile(false);
                            setUploadError('Error al parsear el CSV: ' + err.message);
                        }
                    });
                }
            };

            const restoreBenchmarkDataset = () => {
                setCustomBars([]);
                setDatasetInfo(null);
                setItems(createDefaultCanvasItems());
                resetFilters();
                setExportNotice('Restablecido al Benchmark Oficial LuminoBite (Top 5 Barras).');
                setTimeout(() => setExportNotice(null), 3000);
            };

            '''

text = text[:p_png] + saas_handlers + text[p_png:]
print('Inserted SaaS upload & dataset handlers!')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

