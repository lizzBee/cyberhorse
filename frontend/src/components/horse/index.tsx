import './horse.css'
import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import MetallicBox from '../metallic-box';

export default () => {
    const refContainer = useRef<HTMLDivElement | null>(null);
    useEffect(() => {
        // if (refContainer.current) return
        // === THREE.JS CODE START ===
        var scene = new THREE.Scene();
        const width = window.innerWidth / 2;
        const height = window.innerHeight / 1.5;
        var camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(width, height);
        // document.body.appendChild( renderer.domElement );
        // use ref as a mount point of the Three.js scene instead of the document.body
        refContainer.current && refContainer.current?.appendChild(renderer.domElement);
        var geometry = new THREE.BoxGeometry(1, 1, 1);
        var material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        var cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        camera.position.z = 5;
        var animate = function () {
            requestAnimationFrame(animate);
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
            renderer.render(scene, camera);
        };
        animate();
    }, []);
    return (
        <MetallicBox id='horse-box' >
            <div ref={refContainer}/>
        </MetallicBox >
    );
}