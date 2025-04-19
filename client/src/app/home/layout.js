import SideBar from "../../../components/SideBar";

export const metadata = {
  title: "Main",
  description: "This will be dashboard",
};

export default function HomeLayout({ children }) {
  return (
    <>
        <div className="flex">
            <SideBar />
            <div className="flex-1 ml-64">{children}</div>
        </div>
    </>
  );
}
