const data1 = {
  deviceID: "dh28dslkja",
  deviceType: "LaserCutter",
  timestamp: 1624445837783,
  location: "japan/tokyo/keiyō-industrial-zone/daikibo-factory-meiyo/section-1",
  operationStatus: "healthy",
  temp: 22
};

const data2 = {
  device: { id: "dh28dslkja", type: "LaserCutter" },
  timestamp: "2021-06-23T10:57:17.783Z",
  country: "japan",
  city: "tokyo",
  area: "keiyō-industrial-zone",
  factory: "daikibo-factory-meiyo",
  section: "section-1",
  data: { status: "healthy", temperature: 22 }
};

const expectedResult = {
  deviceID: "dh28dslkja",
  deviceType: "LaserCutter",
  timestamp: 1624445837783,
  location: {
    country: "japan",
    city: "tokyo",
    area: "keiyō-industrial-zone",
    factory: "daikibo-factory-meiyo",
    section: "section-1"
  },
  data: { status: "healthy", temperature: 22 }
};

function convertFromFormat1(obj) {
  const parts = obj.location.split("/");
  return {
    deviceID: obj.deviceID,
    deviceType: obj.deviceType,
    timestamp: obj.timestamp,
    location: {
      country: parts[0],
      city: parts[1],
      area: parts[2],
      factory: parts[3],
      section: parts[4]
    },
    data: {
      status: obj.operationStatus,
      temperature: obj.temp
    }
  };
}

function convertFromFormat2(obj) {
  const dt = new Date(obj.timestamp);
  const timestamp = dt.getTime();
  return {
    deviceID: obj.device.id,
    deviceType: obj.device.type,
    timestamp: timestamp,
    location: {
      country: obj.country,
      city: obj.city,
      area: obj.area,
      factory: obj.factory,
      section: obj.section
    },
    data: obj.data
  };
}

function main(obj) {
  return obj.device ? convertFromFormat2(obj) : convertFromFormat1(obj);
}

function deepEqual(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

const tests = [
  {
    name: "Sanity Test",
    desc: "Ensures the expected result JSON is valid",
    run: () => deepEqual(JSON.parse(JSON.stringify(expectedResult)), expectedResult)
  },
  {
    name: "Data Type 1 Conversion",
    desc: "Converts flat location string format to nested format",
    run: () => deepEqual(main(data1), expectedResult)
  },
  {
    name: "Data Type 2 Conversion",
    desc: "Converts device-object + ISO timestamp format to nested format",
    run: () => deepEqual(main(data2), expectedResult)
  }
];

function renderResults() {
  const results = tests.map(t => {
    try {
      return { ...t, passed: t.run(), error: null };
    } catch (e) {
      return { ...t, passed: false, error: e.message };
    }
  });

  const allPassed = results.every(r => r.passed);

  const summary = document.getElementById("summary");
  summary.textContent = allPassed
    ? `All ${results.length} tests passed`
    : `Some tests failed`;
  summary.className = "summary " + (allPassed ? "pass" : "fail");

  const list = document.getElementById("test-list");
  list.innerHTML = results.map(r => `
    <div class="test-item">
      <div class="test-info">
        <div class="name">${r.name}</div>
        <div class="desc">${r.desc}</div>
        ${r.error ? `<div class="error-msg">Error: ${r.error}</div>` : ""}
      </div>
      <span class="badge ${r.passed ? "pass" : "fail"}">${r.passed ? "PASS" : "FAIL"}</span>
    </div>
  `).join("");

  const output = document.getElementById("output");
  output.textContent = JSON.stringify(main(data1), null, 2);
}

document.addEventListener("DOMContentLoaded", renderResults);
