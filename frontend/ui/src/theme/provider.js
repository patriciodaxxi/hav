/** @jsx jsx */
import { jsx } from "theme-ui";

import { Global, css } from "@emotion/core";

import React from "react";
import { ThemeProvider } from "theme-ui";
import defaultTheme from "./theme";

import * as allComponents from "../components";

export default ({ theme = defaultTheme, children, components = null }) => {
  return (
    <ThemeProvider theme={theme} components={components || allComponents}>
      <Global
        styles={css`
          @import url("https://fonts.googleapis.com/css?family=Noto+Sans|Noto+Serif&display=swap");
          html,
          body {
            margin: 0;
            font-family: "Noto Sans", system-ui, sans-serif;
          }
        `}
      />
      <React.Fragment>{children}</React.Fragment>
    </ThemeProvider>
  );
};
