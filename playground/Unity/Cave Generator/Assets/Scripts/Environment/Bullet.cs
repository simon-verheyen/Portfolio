using UnityEngine;
using System.Collections;

public class Bullet : MonoBehaviour
{
    Rigidbody rigidbody;
    Vector3 velocity;
    
    public int speed;
    
    void Start ()
    {
        rigidbody = GetComponent<Rigidbody>();
        velocity = new Vector3(speed, 0, 0);
    }
    
    void FixedUpdate ()
    {
        rigidbody.MovePosition(rigidbody.position + velocity * Time.fixedDeltaTime);
    }
}