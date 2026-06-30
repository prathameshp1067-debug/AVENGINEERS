const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);

const renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById("bg3d"),
  alpha: true
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x000000, 1);

// Geometry
const geometry = new THREE.TorusKnotGeometry(1.2, 0.35, 120, 16);
const material = new THREE.MeshStandardMaterial({
  color: 0x00ffff,
  metalness: 0.7,
  roughness: 0.2
});
const droneShape = new THREE.Mesh(geometry, material);
scene.add(droneShape);

// Lights
const light = new THREE.PointLight(0xffffff, 2);
light.position.set(5, 5, 5);
scene.add(light);

const ambient = new THREE.AmbientLight(0x404040, 2);
scene.add(ambient);

camera.position.z = 5;

// Animation
function animate() {
  requestAnimationFrame(animate);
  droneShape.rotation.x += 0.01;
  droneShape.rotation.y += 0.015;
  renderer.render(scene, camera);
}
animate();

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
