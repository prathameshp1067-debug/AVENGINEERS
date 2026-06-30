// Handle form submission
document.getElementById("designBtn").addEventListener("click", async () => {
  try {
    const formData = new FormData(document.getElementById("inputForm"));
    const inputs = Object.fromEntries(formData.entries());

    // Collect selections from radio buttons
    inputs.aircraftType = document.querySelector('input[name="aircraftType"]:checked')?.value || "Trainer";
    inputs.wingShape = document.querySelector('input[name="wingShape"]:checked')?.value || "Rectangular";
    inputs.hTail = document.querySelector('input[name="hTail"]:checked')?.value || "Rectangular";
    inputs.vTail = document.querySelector('input[name="vTail"]:checked')?.value || "Single Fin";

    // Send to backend
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(inputs)
    });

    if (!response.ok) throw new Error("Backend error");
    const results = await response.json();
    renderResults(results);
    render3DModel(results);
  } catch (err) {
    console.error(err);
    alert("Calculation failed. Check backend logs.");
  }
});

// Render results into cards
function renderResults(data) {
  document.getElementById("aircraftSummary").innerHTML = `
    <h3>Aircraft Summary</h3>
    <p>Type: ${data.aircraftType}</p>
    <p>Wing: ${data.wingShape}</p>
    <p>Wing Span: ${data.wingSpan} in</p>
    <p>Wing Area: ${data.wingArea} sq.in</p>
    <p>Aspect Ratio: ${data.aspectRatio}</p>
    <p>Payload: ${data.payload} kg</p>
  `;

  document.getElementById("tailSummary").innerHTML = `
    <h3>Tail</h3>
    <p>Horizontal Area: ${data.hTailArea} sq.in</p>
    <p>Vertical Area: ${data.vTailArea} sq.in</p>
    <p>Tail Span: ${data.hTailSpan} in</p>
    <p>Tail Height: ${data.vTailHeight} in</p>
  `;

  document.getElementById("propulsionSummary").innerHTML = `
    <h3>Propulsion</h3>
    <p>Motor: ${data.motor}</p>
    <p>Motor KV: ${data.motorKV}</p>
    <p>ESC: ${data.esc}</p>
    <p>Battery Voltage: ${data.batteryVoltage} V</p>
    <p>Propeller: ${data.propeller}</p>
    <p>Propeller Diameter: ${data.propDiameter} in</p>
    <p>Propeller Pitch: ${data.propPitch} in</p>
    <p>Required Thrust: ${data.requiredThrust} kg</p>
  `;

  document.getElementById("performanceSummary").innerHTML = `
    <h3>Performance</h3>
    <p>Cruise Speed: ${data.cruiseSpeed} km/h</p>
    <p>Max Speed: ${data.maxSpeed} km/h</p>
    <p>Flight Time: ${data.flightTime} min</p>
    <p>Takeoff Distance: ${data.takeoffDistance} m</p>
    <p>Stall Speed: ${data.stallSpeed} km/h</p>
  `;
}

// Render simple 3D model with Three.js
function render3DModel(data) {
  const container = document.getElementById("threeContainer");
  container.innerHTML = ""; // reset

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  // Lighting
  const light = new THREE.PointLight(0xffffff, 1);
  light.position.set(10, 10, 10);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x404040, 1));

  // Wing (box)
  const wingGeometry = new THREE.BoxGeometry(data.wingSpan * 0.05, 0.5, data.wingArea * 0.001);
  const wingMaterial = new THREE.MeshPhongMaterial({ color: 0x00bfff });
  const wing = new THREE.Mesh(wingGeometry, wingMaterial);
  scene.add(wing);

  // Fuselage (cylinder)
  const fuselageGeometry = new THREE.CylinderGeometry(0.3, 0.3, data.fuselageLength || 10, 16);
  const fuselageMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
  const fuselage = new THREE.Mesh(fuselageGeometry, fuselageMaterial);
  fuselage.rotation.z = Math.PI/2;
  scene.add(fuselage);

  camera.position.z = 10;

  function animate() {
    requestAnimationFrame(animate);
    wing.rotation.y += 0.01;
    fuselage.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
  animate();
}
