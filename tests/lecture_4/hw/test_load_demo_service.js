import http from 'k6/http';
import { check, sleep } from 'k6';

const serviceUrl = 'http://localhost:8080';

export let options = {
  stages: [
    { duration: "10m", target: 500 }, 
    { duration: "2m", target: 0 },
  ],
};


export default function () {
  let newUser = {
    username: `testuser_${__VU}_${__ITER}`,
    name: "Sample User",
    birthdate: "2024-10-21",
    password: "strongPassword123"
  };

  let createUserResponse = http.post(
    `${serviceUrl}/user-register`,
    JSON.stringify(newUser),
    { headers: { "Content-Type": "application/json" } }
  );

  check(createUserResponse, {
    'User creation was successful': (r) => r.status === 200,
  });

  sleep(1);
}
