import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:9000"; // Set your backend API base URL here

// Mock localStorage for Node.js
const localStorage = {
  data: {},
  setItem(key, value) {
    this.data[key] = value;
  },
  getItem(key) {
    return this.data[key] || null;
  },
  removeItem(key) {
    delete this.data[key];
  },
  clear() {
    this.data = {};
  }
};

const login = async ({ email, password }) => {
  try {
    const response = await axios.post("/api/accounts/login/", {
      email,
      password,
    });

    // response.data contains the login result
    console.log(response.data);

    // Store tokens securely (in a real app, use httpOnly cookies for refresh token)
    const { access, refresh, user } = response.data.data;
    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    localStorage.setItem("user", JSON.stringify(user));

    return response.data;
  } catch (error) {
    console.error("Login failed:", error.response?.data || error.message);
    throw error;
  }
};

// Example: Use stored token for authenticated requests
// const getRoadmap = async () => {
//   const accessToken = localStorage.getItem("accessToken");
//   if (!accessToken) {
//     console.error("No access token found. Please login first.");
//     return;
//   }

//   try {
//     const response = await axios.get("/api/core/roadmap/", {
//       headers: {
//         Authorization: `Bearer ${accessToken}`,
//         "Content-Type": "application/json",
//       },
//     });
//     console.log("Roadmap:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Failed to get roadmap:", error.response?.data || error.message);
//     throw error;
//   }
// };

// Example: Create roadmap
const createRoadmap = async (payload) => {
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    console.error("No access token found. Please login first.");
    return;
  }

  try {
    const response = await axios.post("/api/core/create-roadmap/", payload, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    });
    console.log("Roadmap created:", response.data);
    return response.data;
  } catch (error) {
    console.error("Failed to create roadmap:", error.response?.data || error.message);
    throw error;
  }
};

// Usage examples (uncomment to test)
(async () => {
  try {
    // Example login
    await login({ email: "admin@gmail.com", password: "123456@Ad" });
    
    // Example get roadmap
    // await getRoadmap();
    
    // Example create roadmap
    await createRoadmap({
      subjects: ["Math", "English"],
      exam_date: "2023-12-31",
      goal: "Pass the exam",
      quiz_result: []
    });
  } catch (error) {
    console.error("Test failed:", error.message);
  }
})();
