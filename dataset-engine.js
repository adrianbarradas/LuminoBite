// LuminoBite Intelligent Dataset Normalizer & Heuristic Parser (Zero-Template Engine)
// Infers column semantics, cleans nutrient metrics, and standardizes arbitrary CSV/Excel rows into BI products

window.LuminoDatasetEngine = {
    // Column semantic matchers (case-insensitive, normalized accents)
    KEYWORD_MAP: {
        name: ['nombre', 'name', 'producto', 'product', 'item', 'titulo', 'title', 'marca', 'brand', 'label', 'referencia'],
        flavor: ['sabor', 'flavor', 'flavour', 'variedad', 'variety', 'tipo', 'subtitulo', 'linea', 'desc', 'descripcion'],
        calories: ['calorias', 'calories', 'caloria', 'kcal', 'energia', 'energy', 'cal'],
        protein: ['proteina', 'protein', 'proteinas', 'prot', 'prots', 'pro'],
        totalFat: ['grasa total', 'grasas totales', 'grasa', 'total fat', 'fat', 'grasas', 'lipidos', 'lipid'],
        satFat: ['grasa saturada', 'grasas saturadas', 'sat fat', 'saturated fat', 'saturadas', 'sat', 'saturada'],
        transFat: ['grasa trans', 'trans fat', 'trans'],
        totalCarbs: ['carbohidratos totales', 'carbohidratos', 'carbs', 'total carbs', 'total carbohydrate', 'hidratos', 'hc'],
        netCarbs: ['carbos netos', 'carbohidratos netos', 'net carbs', 'net carb', 'carbohidratos disponibles', 'net'],
        fiber: ['fibra dietetica', 'fibra', 'fiber', 'dietary fiber', 'fibra alimentaria', 'fibras'],
        totalSugars: ['azucares totales', 'azucares', 'azucar', 'sugars', 'total sugars', 'sugar'],
        addedSugars: ['azucares anadidos', 'added sugars', 'anadidos', 'azucar anadida'],
        polyols: ['alcoholes de azucar', 'polioles', 'polyols', 'sugar alcohols', 'poliol', 'maltitol', 'eritritol', 'erythritol'],
        servingGrams: ['porcion', 'serving', 'serving size', 'gramos', 'grams', 'peso', 'weight', 'g', 'tamano porcion'],
        sodium: ['sodio', 'sodium', 'na', 'sal', 'salt'],
        cholesterol: ['colesterol', 'cholesterol', 'col'],
        calcium: ['calcio', 'calcium', 'ca'],
        potassium: ['potasio', 'potassium', 'k'],
        iron: ['hierro', 'iron', 'fe'],
        vitD: ['vitamina d', 'vitamin d', 'vit d', 'vit_d'],
        ingredients: ['ingredientes', 'ingredients', 'formula', 'composicion', 'ingrediente', 'componentes'],
        allergens: ['alergenos', 'allergens', 'contiene', 'contains', 'trazas', 'traces', 'alergeno', 'alergias']
    },

    cleanString(val) {
        if (!val) return '';
        return String(val)
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .trim();
    },

    parseNumber(val, defaultVal = 0) {
        if (typeof val === 'number') return isNaN(val) ? defaultVal : val;
        if (!val) return defaultVal;
        const cleaned = String(val)
            .replace(/,/g, '.')
            .replace(/[^0-9.-]/g, '');
        const n = parseFloat(cleaned);
        return isNaN(n) ? defaultVal : n;
    },

    // Identifies column mapping automatically
    detectColumnMapping(headers) {
        const mapping = {};
        const normalizedHeaders = headers.map(h => ({
            raw: h,
            norm: this.cleanString(h)
        }));

        for (const [key, keywords] of Object.entries(this.KEYWORD_MAP)) {
            let matchedHeader = null;
            // 1. Exact or startsWith match
            for (const kw of keywords) {
                const found = normalizedHeaders.find(h => h.norm === kw || h.norm.startsWith(kw + ' ') || h.norm.endsWith(' ' + kw));
                if (found) {
                    matchedHeader = found.raw;
                    break;
                }
            }
            // 2. Substring match
            if (!matchedHeader) {
                for (const kw of keywords) {
                    const found = normalizedHeaders.find(h => h.norm.includes(kw));
                    if (found) {
                        matchedHeader = found.raw;
                        break;
                    }
                }
            }
            if (matchedHeader) {
                mapping[key] = matchedHeader;
            }
        }
        return mapping;
    },

    // Infers relevant biometric / allergen tags based on ingredients & text
    inferTags(rowText) {
        const text = this.cleanString(rowText);
        const tags = [];
        if (text.includes('leche') || text.includes('milk') || text.includes('whey') || text.includes('suero') || text.includes('casein') || text.includes('lacteo')) tags.push('milk');
        if (text.includes('soya') || text.includes('soy') || text.includes('lecitina') || text.includes('lecithin')) tags.push('soy');
        if (text.includes('almendra') || text.includes('almond') || text.includes('nuez') || text.includes('nut')) tags.push('almond');
        if (text.includes('mani') || text.includes('peanut') || text.includes('cacahuate')) tags.push('peanut');
        if (text.includes('huevo') || text.includes('egg') || text.includes('albumina')) tags.push('egg');
        if (text.includes('colageno') || text.includes('collagen')) tags.push('collagen');
        if (text.includes('maltitol') || text.includes('poliol') || text.includes('eritritol') || text.includes('xylitol') || text.includes('sorbitol')) tags.push('maltitol');
        if (text.includes('datil') || text.includes('date')) tags.push('dates');
        if (text.includes('cacao') || text.includes('cocoa') || text.includes('chocolate')) tags.push('cocoa');
        if (text.includes('fibra') || text.includes('fiber') || text.includes('inulina') || text.includes('prebiot')) tags.push('fiber');
        if (text.includes('gluten free') || text.includes('sin gluten') || text.includes('libre de gluten')) tags.push('gluten_free');
        if (text.includes('keto') || text.includes('cetogen')) tags.push('keto');
        return tags.length > 0 ? tags : ['custom'];
    },

    // Generates high-class brand colors dynamically
    palette: [
        { brand: '#1E40AF', accent: '#60A5FA' }, // Indigo Royal
        { brand: '#780030', accent: '#F73282' }, // Lumino Burgundy / Pink
        { brand: '#047857', accent: '#34D399' }, // Emerald Biotech
        { brand: '#B45309', accent: '#FBBF24' }, // Amber Artisan
        { brand: '#6D28D9', accent: '#A78BFA' }, // Violet Lab
        { brand: '#0E7490', accent: '#38BDF8' }, // Cyan Tech
        { brand: '#BE123C', accent: '#FB7185' }, // Rose Berry
        { brand: '#15803D', accent: '#86EFAC' }, // Clean Botanical
        { brand: '#374151', accent: '#9CA3AF' }  // Dark Mineral
    ],

    // Transforms arbitrary raw rows into standardized LuminoBite product models
    normalizeRows(rawRows) {
        if (!Array.isArray(rawRows) || rawRows.length === 0) return [];
        const headers = Object.keys(rawRows[0]);
        const map = this.detectColumnMapping(headers);

        return rawRows.map((row, idx) => {
            const getVal = (key) => map[key] ? row[map[key]] : undefined;

            const name = String(getVal('name') || row[headers[0]] || `Producto BI-${idx + 1}`).trim();
            const flavor = String(getVal('flavor') || row[headers[1]] || 'Fórmula Estándar').trim();

            const servingGrams = this.parseNumber(getVal('servingGrams'), 60);
            const calories = this.parseNumber(getVal('calories'), 200);
            const protein = this.parseNumber(getVal('protein'), 20);
            const totalFat = this.parseNumber(getVal('totalFat'), 8);
            const satFat = this.parseNumber(getVal('satFat'), Math.round(totalFat * 0.35));
            const transFat = this.parseNumber(getVal('transFat'), 0);
            const totalCarbs = this.parseNumber(getVal('totalCarbs'), 22);
            const fiber = this.parseNumber(getVal('fiber'), 8);
            const polyols = this.parseNumber(getVal('polyols'), 6);
            
            // Intelligent net carbs calculation if missing
            let netCarbs = this.parseNumber(getVal('netCarbs'), null);
            if (netCarbs === null) {
                netCarbs = Math.max(0, Math.round((totalCarbs - fiber - (polyols * 0.5)) * 10) / 10);
            }

            const totalSugars = this.parseNumber(getVal('totalSugars'), 2);
            const addedSugars = this.parseNumber(getVal('addedSugars'), 0);
            const sodium = this.parseNumber(getVal('sodium'), 180);
            const cholesterol = this.parseNumber(getVal('cholesterol'), 5);
            const calcium = this.parseNumber(getVal('calcium'), 120);
            const potassium = this.parseNumber(getVal('potassium'), 110);
            const iron = this.parseNumber(getVal('iron'), 2.2);
            const vitD = this.parseNumber(getVal('vitD'), 0);

            const rowConcat = Object.values(row).join(' ');
            const ingredientsES = String(getVal('ingredients') || `Mezcla patentada de aislado proteico (${name}), fibra prebiótica soluble, lípidos funcionales, aromas naturales y minerales esenciales.`);
            const allergens = String(getVal('allergens') || 'Procesado en planta con control biotecnológico.');
            const tags = this.inferTags(rowConcat + ' ' + name + ' ' + flavor);

            const colorPair = this.palette[idx % this.palette.length];

            return {
                id: `custom_${idx + 1}_${Date.now().toString(36)}`,
                name,
                flavor,
                brandColor: colorPair.brand,
                accentColor: colorPair.accent,
                servingGrams,
                calories,
                protein,
                totalFat,
                satFat,
                transFat,
                cholesterol,
                sodium,
                totalCarbs,
                fiber,
                totalSugars,
                addedSugars,
                polyols,
                polyolType: polyols > 0 ? 'Polioles / Alcoholes' : 'Cero Polioles',
                netCarbs,
                vitD,
                calcium,
                iron,
                potassium,
                ingredientsES,
                containsVerbatim: `Contiene ingredientes de ${tags.join(', ')}`,
                tracesVerbatim: allergens,
                tags,
                isCustomImport: true
            };
        });
    },

    // Generates an automated, fully populated, intelligent canvas layout tailored to any custom dataset
    generateDatasetCanvas(products, title = 'DASHBOARD INTELIGENTE DE I+D') {
        const items = [];
        const topBarCount = Math.min(products.length, 6);
        const topProducts = products.slice(0, topBarCount);

        // 1. Executive Banner
        items.push({
            uid: `header_${Date.now()}`,
            type: 'title_banner',
            x: 40,
            y: 24,
            w: 880,
            h: 96,
            z: 2,
            title: title.toUpperCase(),
            subtitle: `Dataset empresarial procesado automáticamente: ${products.length} fórmulas detectadas, KPIs unificados y benchmarks de biodisponibilidad.`
        });

        // 2. Interactive Analytical Filter Widgets
        items.push({
            uid: 'widget_macro_sculptor',
            type: 'macro_sculptor',
            x: 40,
            y: 136,
            w: 390,
            h: 410,
            z: 10
        });

        items.push({
            uid: 'widget_scatter_filter',
            type: 'scatter_matrix',
            x: 40,
            y: 564,
            w: 390,
            h: 360,
            z: 10
        });

        // 3. Grid of Product Cards
        topProducts.forEach((p, idx) => {
            const col = idx % 3;
            const row = Math.floor(idx / 3);
            items.push({
                uid: `card_${p.id}_${idx}`,
                type: 'bar_card',
                barId: p.id,
                x: 455 + col * 330,
                y: 136 + row * 385,
                w: 310,
                h: 365,
                z: 5,
                config: {
                    customTitle: p.name,
                    customFlavor: p.flavor,
                    brandColor: p.brandColor,
                    accentColor: p.accentColor,
                    shape: idx % 2 === 0 ? 'rounded' : 'pill',
                    gradientType: 'linear'
                }
            });
        });

        // 4. BI Analytics Charts tailored to dataset metrics
        items.push({
            uid: `chart_bi_protein_${Date.now()}`,
            type: 'custom_chart',
            x: 455,
            y: 136 + (Math.ceil(topBarCount / 3)) * 385,
            w: 480,
            h: 330,
            z: 6,
            config: {
                title: 'Benchmarking de Proteína por Porción (g)',
                chartType: 'ranking',
                metric: 'protein',
                primaryColor: '#146779',
                accentColor: '#38BDF8',
                showLabels: true,
                showGrid: true
            }
        });

        items.push({
            uid: `chart_bi_calories_${Date.now()}`,
            type: 'custom_chart',
            x: 955,
            y: 136 + (Math.ceil(topBarCount / 3)) * 385,
            w: 480,
            h: 330,
            z: 6,
            config: {
                title: 'Eficiencia Calórica vs. Carbos Netos',
                chartType: 'scatter',
                metric: 'protein',
                secondaryMetric: 'netCarbs',
                primaryColor: '#780030',
                accentColor: '#F73282',
                showLabels: true,
                showGrid: true
            }
        });

        // 5. Radar comparison widget
        items.push({
            uid: `widget_radar_${Date.now()}`,
            type: 'radar_chart',
            x: 1455,
            y: 136,
            w: 420,
            h: 365,
            z: 6
        });

        return items;
    }
};

