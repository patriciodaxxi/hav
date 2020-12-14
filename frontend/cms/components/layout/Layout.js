import React from "react";

const Wrapper = ({ children }) => {
  return (
    <div className="flex flex-col md:flex-row md:items-stretch md:h-screen md:w-screen">
      {children}
    </div>
  );
};

const Nav = ({ children }) => {
  return (
    <div className="flex-initial md:w-1/5 md:min-h-screen bg-yellow-400">
      {children}
    </div>
  );
};

const Main = ({ children }) => {
  return (
    <div className="flex-grow p-4 md:overflow-y-scroll md:overflow-x-hidden min-h-screen">
      {children}
    </div>
  );
};

export default { Wrapper, Nav, Main };
