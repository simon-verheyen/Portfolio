using UnityEngine;
using System.Collections;

public class Player : MonoBehaviour
{
    Rigidbody rigidbody;
    Vector3 velocity;
    
    public Object bullet;

	void Start ()
    {
        rigidbody = GetComponent<Rigidbody>();
	}
	
	void Update ()
    {
        velocity = new Vector3(Input.GetAxisRaw("Horizontal"), 0, Input.GetAxisRaw("Vertical")).normalized * 10;
        if (Input.GetMouseButtonDown(0))
            shoot();
    }

    void FixedUpdate ()
    {
        rigidbody.MovePosition(rigidbody.position + velocity * Time.fixedDeltaTime);
    }
    
    void shoot()
    {
        Instantiate(bullet, rigidbody.position, Quaternion.identity);
    }
    
    
}
