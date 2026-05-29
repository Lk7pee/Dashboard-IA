const dashboardDataElement = document.getElementById("dashboardData");
const dashboardData = dashboardDataElement ? JSON.parse(dashboardDataElement.textContent) : {};

const colors = {
    blue: "#0f55c8",
    blueDark: "#09357c",
    green: "#159447",
    teal: "#0aa1a7",
    purple: "#7a45c7",
    amber: "#c98513",
    red: "#d84b6b",
    text: "#13213c",
    muted: "#64728a",
    lightText: "#f5f8ff",
};

const countryColors = {
    Global: "#0f55c8",
    EUA: "#159447",
    China: "#d84b6b",
    "Reino Unido": "#7a45c7",
    Brasil: "#c98513",
};

const toolColors = [colors.blue, colors.green, colors.purple, colors.amber, colors.red, colors.teal];
const plotConfig = {
    displayModeBar: false,
    responsive: true,
};

function isDarkTheme() {
    return document.body.classList.contains("dark-theme");
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
        // Navegadores podem bloquear localStorage quando o HTML e aberto por arquivo.
    }
}

function chartTheme() {
    const dark = isDarkTheme();
    return {
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
            color: dark ? colors.lightText : colors.text,
            family: "Arial, Helvetica, sans-serif",
        },
        xaxis: {
            gridcolor: dark ? "rgba(255,255,255,0.1)" : "rgba(19,33,60,0.1)",
            zerolinecolor: dark ? "rgba(255,255,255,0.14)" : "rgba(19,33,60,0.14)",
        },
        yaxis: {
            gridcolor: dark ? "rgba(255,255,255,0.1)" : "rgba(19,33,60,0.1)",
            zerolinecolor: dark ? "rgba(255,255,255,0.14)" : "rgba(19,33,60,0.14)",
        },
    };
}

function baseLayout(extraLayout = {}) {
    const theme = chartTheme();
    return {
        ...theme,
        margin: isNarrowScreen()
            ? { t: 44, r: 14, b: 56, l: 48 }
            : { t: 38, r: 26, b: 56, l: 62 },
        hovermode: "closest",
        legend: {
            orientation: "h",
            x: 0,
            y: 1.15,
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
            color: countryColors[country] || colors.blue,
            width: selectedMode ? 4 : 3,
            shape: "spline",
        },
        marker: {
            size: selectedMode ? 9 : 7,
            color: countryColors[country] || colors.blue,
            line: { color: "#ffffff", width: 1 },
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

function renderIndicatorChart() {
    const indicators = dashboardData.investimentos?.indicadores || [];
    const chart = document.getElementById("indicatorChart");

    if (!chart || !indicators.length) {
        return;
    }

    const countries = indicators.map((item) => item.pais);
    const realized = indicators.map((item) => item.realizado);
    const average = indicators.map((item) => item.media_historica);

    const traces = [
        {
            x: countries,
            y: realized,
            type: "bar",
            name: "Último ano",
            marker: { color: colors.green },
            hovertemplate: "%{x}<br>Último ano: US$ %{y:.2f} bi<extra></extra>",
        },
        {
            x: countries,
            y: average,
            type: "scatter",
            mode: "markers",
            name: "Média histórica",
            marker: {
                color: colors.blue,
                size: 10,
                symbol: "diamond",
            },
            hovertemplate: "%{x}<br>Média histórica: US$ %{y:.2f} bi<extra></extra>",
        },
    ];

    const layout = baseLayout({
        margin: { t: 38, r: 12, b: isNarrowScreen() ? 80 : 58, l: 48 },
        barmode: "group",
        xaxis: {
            ...chartTheme().xaxis,
            tickangle: isNarrowScreen() ? -30 : 0,
        },
        yaxis: {
            ...chartTheme().yaxis,
            title: "US$ bi",
            rangemode: "tozero",
        },
    });

    Plotly.newPlot("indicatorChart", traces, layout, plotConfig);
}

function renderAdoptionDonut() {
    const chart = document.getElementById("adoptionDonut");
    if (!chart) {
        return;
    }

    const average = Number(dashboardData.setores?.media || 0);
    const remaining = Math.max(0, 100 - average);

    const trace = {
        values: [average, remaining],
        labels: ["Adoção média", "Potencial"],
        type: "pie",
        hole: 0.68,
        marker: { colors: [colors.green, "#dfe6f0"] },
        textinfo: "none",
        hovertemplate: "%{label}: %{value:.1f}%<extra></extra>",
    };

    const layout = baseLayout({
        showlegend: false,
        margin: { t: 8, r: 8, b: 8, l: 8 },
        annotations: [
            {
                text: `<b>${average.toFixed(1)}%</b><br>Adoção`,
                x: 0.5,
                y: 0.5,
                showarrow: false,
                font: {
                    size: isNarrowScreen() ? 20 : 24,
                    color: isDarkTheme() ? colors.lightText : colors.green,
                },
            },
        ],
    });

    Plotly.newPlot("adoptionDonut", [trace], layout, plotConfig);
}

function renderSectorChart() {
    const chart = document.getElementById("sectorChart");
    if (!chart) {
        return;
    }

    const trace = {
        x: dashboardData.setores.percentuais,
        y: dashboardData.setores.nomes,
        type: "bar",
        orientation: "h",
        marker: {
            color: dashboardData.setores.percentuais,
            colorscale: [
                [0, "#b7d7ff"],
                [0.55, colors.blue],
                [1, colors.green],
            ],
            line: { color: "rgba(19,33,60,0.18)", width: 1 },
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
    const chart = document.getElementById("trafficChart");
    if (!chart) {
        return;
    }

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
    renderIndicatorChart();
    renderAdoptionDonut();
    renderSectorChart();
    renderTrafficChart();
}

function setupThemeToggle() {
    const savedTheme = safeLocalStorageGet("dashboard-governance-theme");
    const button = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");

    if (!button || !icon) {
        return;
    }

    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        icon.textContent = "☀";
    }

    button.addEventListener("click", () => {
        document.body.classList.toggle("dark-theme");
        const dark = isDarkTheme();
        icon.textContent = dark ? "☀" : "◐";
        safeLocalStorageSet("dashboard-governance-theme", dark ? "dark" : "light");
        renderAllCharts();
    });
}

function revealCards() {
    document.querySelectorAll(".reveal-card").forEach((card, index) => {
        window.setTimeout(() => card.classList.add("is-visible"), 100 * index);
    });
}

function setupRefreshButton() {
    const button = document.getElementById("refreshDashboard");
    if (!button) {
        return;
    }

    button.addEventListener("click", () => {
        renderAllCharts();
        button.classList.add("is-updated");
        window.setTimeout(() => button.classList.remove("is-updated"), 450);
    });
}

function setupResizeHandler() {
    let resizeTimer;
    window.addEventListener("resize", () => {
        if (typeof Plotly === "undefined") {
            return;
        }

        window.clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(renderAllCharts, 180);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupThemeToggle();
    populateCountrySelect();
    revealCards();
    setupRefreshButton();
    renderAllCharts();
    setupResizeHandler();
});
