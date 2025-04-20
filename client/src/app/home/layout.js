import SideBar from "../../../components/SideBar";

export const metadata = {
  title: "Main",
  description: "This will be dashboard",
};

export default function HomeLayout({ children }) {
  return (
    <>
        <div className="flex h-screen">
            <SideBar />
            <div className="flex-1 ml-64 bg-[#060a14]">{children}</div>
        </div>
    </>
  );
}
