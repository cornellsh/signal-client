module.exports = {
  ci: {
    collect: {
      staticDistDir: "site",
      url: ["http://localhost:8000/"],
      startServerCommand: "python3 -m http.server 8000 -d site",
      numberOfRuns: 1,
    },
    assert: {
      assertions: {
        "categories:performance": ["warn", { "minScore": 0.8 }],
        "categories:accessibility": ["warn", { "minScore": 0.9 }]
      }
    },
    upload: {
      target: "filesystem",
      outputDir: "lighthouse-artifacts"
    }
  }
};
