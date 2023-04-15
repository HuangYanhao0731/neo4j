document.addEventListener("DOMContentLoaded", function () {
  // 获取存在页面中的图谱数据
  const graphData = JSON.parse(document.getElementById("graph-data").textContent);

  // 使用Cytoscape库创建知识图谱可视化
  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: graphData,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#6fb3b8",
          label: "data(name)",
          "text-valign": "center",
          "text-halign": "center",
          "font-size": "12px",
          "text-outline-color": "#6fb3b8",
          "text-outline-width": "2px",
          color: "#fff",
        },
      },
      {
        selector: "edge",
        style: {
          width: "2px",
          "line-color": "#a8eae5",
          "curve-style": "bezier",
          "target-arrow-color": "#a8eae5",
          "target-arrow-shape": "triangle",
          label: "data(label)",
          "font-size": "10px",
          "text-outline-color": "#a8eae5",
          "text-outline-width": "1px",
          color: "#333",
                },
      },
            ],
            layout: {
          name: "cose",
          idealEdgeLength: 100,
          nodeOverlap: 20,
          refresh: 20,
          fit: true,
          padding: 30,
          randomize: false,
          componentSpacing: 100,
          nodeRepulsion: 400000,
          edgeElasticity: 100,
          nestingFactor: 5,
          gravity: 80,
          numIter: 1000,
          initialTemp: 200,
          coolingFactor: 0.95,
          minTemp: 1.0,
        },
    });
});

