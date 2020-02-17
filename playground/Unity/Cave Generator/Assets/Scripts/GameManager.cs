using UnityEngine;

using System;
using System.Collections;
using System.Collections.Generic;


public class GameManager : MonoBehaviour
{

    public GameObject map;
    public GameObject player;
    public GameObject enemy;

    public string seed;
    public bool useRandomSeed;

    //public MeshFilter walls;
    //public MeshFilter cave;
    private MapGenerator mapGen;
    private Vector3 playerSpawn;
    private Vector3 exitSpwan;



    void Start()
    {

        /*if (useRandomSeed)
            seed = Time.time.ToString();
        map.MapGenerator.GenerateMap(seed);
        mapGenerator = Instantiate(mapGenerator, transform.position, transform.rotation) as GameObject;
        mapGenerator = mapGenerator.GetComponent<MapGenerator>();*/

        mapGen = map.GetComponent<MapGenerator>();
        if (useRandomSeed)
            seed = Time.time.ToString();
        mapGen.GenerateMap(seed);

        playerSpawn = mapGen.FindStartArea();
        Instantiate(player, playerSpawn, Quaternion.identity);

        //exitSpawn = mapGen.FindEndArea();
        //Instantiate(exit, exitSpawn, Quaternion.identity)

    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            if (useRandomSeed)
                seed = Time.time.ToString();
            mapGen.GenerateMap(seed);
            
            /*if (useRandomSeed)
                seed = Time.time.ToString();
            map.MapGenerator.GenerateMap(seed);

            /*walls.mesh = wallMesh;

            MeshCollider wallCollider = walls.gameObject.AddComponent<MeshCollider>();
            wallCollider.sharedMesh = wallMesh;*/

            //mapGen.GenerateMap();
        }
    }
}
