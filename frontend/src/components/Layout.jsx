import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />

      <div style={{ flex: 1, background: "#3b485b" }}>
        <Navbar />

        <div style={{ padding: "25px" }}>
          {children}
        </div>
      </div>
    </div>
  );
}