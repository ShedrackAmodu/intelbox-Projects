import { Flex, Button, Container } from "@chakra-ui/react";
import Category from "./components/Category";
import Intro from "./components/Intro";
import { useState } from "react";
import "./app.css";

const App = () => {
  const [isClicked, setIsClicked] = useState(false);

  const handleClick = () => {
    setIsClicked(true);
  };
  return (
    <Container
      id="box"
      minH="100vh"
      maxW="100%"
      pt="50px"
      align="center"
      color="white"
    >
      <Flex
        id="backdrop"
        backdropFilter="auto"
        backdropInvert="20%"
        backdropBlur="2px"
        align="center"
        flexDir="column"
        gap="50px"
        py="20px"
        w={{ sm: "80%", md: " 60%" }}
        borderRadius="10px"
      >
        {!isClicked ? (
          <>
            {" "}
            <Intro />
            <Button onClick={handleClick}>Click to start</Button>
          </>
        ) : (
          <Category />
        )}
      </Flex>
    </Container>
  );
};

export default App;
