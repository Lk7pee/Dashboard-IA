const dashboardDataElement = document.getElementById("dashboardData");
const dashboardData = dashboardDataElement ? JSON.parse(dashboardDataElement.textContent) : {};

const colors = {
    cyan: "#42d8ff",
    violet: "#9b7cff",
    green: "#35e0a1",
    yellow: "#ffd166",
    red: "#ff6b8a",
    blue: "#4da3ff",
    orange: "#ff9f43",
    textDark: "#f5f8ff",
    textLight: "#0d1729",
};

const countryColors = {
    Global: colors.cyan,
    EUA: colors.green,
    China: colors.red,
    "Reino Unido": colors.violet,
    Brasil: colors.yellow,
};

const toolColors = [colors.cyan, colors.violet, colors.green, colors.yellow, colors.red, colors.blue];
const plotConfig = {
    displayModeBar: false,
    responsive: true,
};

function isLightTheme() {
    return document.body.classList.contains("light-theme");
}

function isNarrowScreen() {
    return window.innerWidth <= 640;
}

function safeLocalStorageGet(key) {
    try {
        return localStorage.getItem(key);
    } catch {
        return null;
    }
}

function safeLocalStorageSet(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch {
        // A abertura direta por arquivo pode bloquear localStorage em alguns navegadores.
    }
}

function chartTheme() {
    const light = isLightTheme();
    return {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
            color: light ? colors.textLight : colors.textDark,
            family: "Arial, Helvetica, sans-serif",
        },
        xaxis: {
            gridcolor: light ? "rgba(13,23,41,0.1)" : "rgba(255,255,255,0.1)",
            zerolinecolor: light ? "rgba(13,23,41,0.14)" : "rgba(255,255,255,0.14)",
        },
        yaxis: {
            gridcolor: light ? "rgba(13,23,41,0.1)" : "rgba(255,255,255,0.1)",
            zerolinecolor: light ? "rgba(13,23,41,0.14)" : "rgba(255,255,255,0.14)",
        },
    };
}

function baseLayout(extraLayout = {}) {
    const theme = chartTheme();
    return {
        ...theme,
        margin: isNarrowScreen()
            ? { t: 42, r: 12, b: 56, l: 44 }
            : { t: 34, r: 26, b: 56, l: 62 },
        hovermode: "closest",
        legend: {
            orientation: "h",
            x: 0,
            y: 1.14,
            font: { size: isNarrowScreen() ? 10 : 12 },
        },
        ...extraLayout,
    };
}

function investmentOrder() {
    const configuredOrder = dashboardData.investimentos?.ordem || [];
    const availableCountries = Object.keys(dashboardData.investimentos?.paises || {});
    return configuredOrder.length ? configuredOrder : availableCountries;
}

function populateCountrySelect() {
    const select = document.getElementById("countrySelect");
    if (!select) {
        return;
    }

    const countries = investmentOrder();
    select.innerHTML = "";

    const allOption = document.createElement("option");
    allOption.value = "todos";
    allOption.textContent = "Todos os países";
    select.appendChild(allOption);

    countries.forEach((country) => {
        const option = document.createElement("option");
        option.value = country;
        option.textContent = country;
        select.appendChild(option);
    });

    select.addEventListener("change", () => renderInvestmentChart(select.value));
}

function createInvestmentTrace(country, source, selectedMode = false) {
    return {
        x: source.anos,
        y: source.valores,
        type: "scatter",
        mode: "lines+markers",
        name: country,
        line: {
            color: countryColors[country] || colors.cyan,
            width: selectedMode ? 4 : 3,
            shape: "spline",
        },
        marker: {
            size: selectedMode ? 9 : 7,
            color: countryColors[country] || colors.cyan,
            line: { color: "rgba(255,255,255,0.35)", width: 1 },
        },
        hovertemplate: `${country}<br>Ano %{x}<br>US$ %{y:.2f} bi<extra></extra>`,
    };
}

function renderInvestmentChart(selected = "todos") {
    const countries = dashboardData.investimentos?.paises || {};
    const chart = document.getElementById("investmentChart");

    if (!chart) {
        return;
    }

    if (!Object.keys(countries).length) {
        chart.innerHTML = "<p class='chart-error'>Não há dados reais de investimento disponíveis para exibir.</p>";
        return;
    }

    const traces = selected === "todos"
        ? investmentOrder()
            .filter((country) => countries[country])
            .map((country) => createInvestmentTrace(country, countries[country]))
        : [createInvestmentTrace(selected, countries[selected], true)];

    const layout = baseLayout({
        xaxis: {
            ...chartTheme().xaxis,
            title: "Ano",
            tickmode: "linear",
            dtick: 1,
        },
        yaxis: {
            ...chartTheme().yaxis,
            title: isNarrowScreen() ? "US$ bi" : "Investimento em bilhões de dólares",
            rangemode: "tozero",
        },
    });

    Plotly.newPlot("investmentChart", traces, layout, plotConfig);
}

function renderSectorChart() {
    const trace = {
        x: dashboardData.setores.percentuais,
        y: dashboardData.setores.nomes,
        type: "bar",
        orientation: "h",
        marker: {
            color: dashboardData.setores.percentuais,
            colorscale: [
                [0, colors.blue],
                [0.55, colors.cyan],
                [1, colors.green],
            ],
            line: { color: "rgba(255,255,255,0.18)", width: 1 },
        },
        hovertemplate: "%{y}<br>%{x:.0f}% de adoção<extra></extra>",
    };

    const layout = baseLayout({
        margin: isNarrowScreen()
            ? { t: 20, r: 12, b: 44, l: 118 }
            : { t: 18, r: 28, b: 46, l: 150 },
        showlegend: false,
        xaxis: {
            ...chartTheme().xaxis,
            title: "Percentual de adoção",
            range: [0, 100],
            ticksuffix: "%",
        },
        yaxis: {
            ...chartTheme().yaxis,
            automargin: true,
        },
    });

    Plotly.newPlot("sectorChart", [trace], layout, plotConfig);
}

function renderTrafficChart() {
    const traces = Object.entries(dashboardData.trafego).map(([tool, source], index) => ({
        x: source.anos,
        y: source.valores,
        type: "scatter",
        mode: "lines+markers",
        name: tool,
        line: { color: toolColors[index % toolColors.length], width: 3, shape: "spline" },
        marker: { size: 7 },
        hovertemplate: `${tool}<br>Ano %{x}<br>%{y:.0f} milhões<extra></extra>`,
    }));

    const layout = baseLayout({
        margin: isNarrowScreen()
            ? { t: 62, r: 12, b: 52, l: 46 }
            : { t: 50, r: 28, b: 52, l: 62 },
        xaxis: {
            ...chartTheme().xaxis,
            title: "Ano",
            tickmode: "linear",
            dtick: 1,
        },
        yaxis: {
            ...chartTheme().yaxis,
            title: isNarrowScreen() ? "Milhões" : "Usuários em milhões",
            rangemode: "tozero",
        },
    });

    Plotly.newPlot("trafficChart", traces, layout, plotConfig);
}

function renderAllCharts() {
    if (typeof Plotly === "undefined") {
        document.querySelectorAll(".chart").forEach((chart) => {
            chart.innerHTML = "<p class='chart-error'>Não foi possível carregar a biblioteca de gráficos.</p>";
        });
        return;
    }

    const select = document.getElementById("countrySelect");
    renderInvestmentChart(select?.value || "todos");
    renderSectorChart();
    renderTrafficChart();
}

function setupThemeToggle() {
    const savedTheme = safeLocalStorageGet("dashboard-theme");
    const button = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");

    if (!button || !icon) {
        return;
    }

    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
        icon.textContent = "☀";
    }

    button.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");
        const light = isLightTheme();
        icon.textContent = light ? "☀" : "◐";
        safeLocalStorageSet("dashboard-theme", light ? "light" : "dark");
        renderAllCharts();
    });
}

function revealCards() {
    document.querySelectorAll(".reveal-card").forEach((card, index) => {
        window.setTimeout(() => card.classList.add("is-visible"), 110 * index);
    });
}

function setupCardInteraction() {
    document.querySelectorAll(".summary-card").forEach((card) => {
        card.addEventListener("mousemove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            card.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(66,216,255,0.16), transparent 8rem), linear-gradient(180deg, var(--panel), rgba(255,255,255,0.03))`;
        });

        card.addEventListener("mouseleave", () => {
            card.style.background = "";
        });
    });
}

function setupResizeHandler() {
    window.addEventListener("resize", () => {
        if (typeof Plotly === "undefined") {
            return;
        }

        renderAllCharts();
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupThemeToggle();
    populateCountrySelect();
    revealCards();
    setupCardInteraction();
    renderAllCharts();
    setupResizeHandler();
});
