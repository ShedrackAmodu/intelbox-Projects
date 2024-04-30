import { Text, Flex, VStack, Heading } from "@chakra-ui/react";
import { useState } from "react";
import Trivia from "./Trivia"; // Make sure this import is correct
import { MdOutlineScience } from "react-icons/md";
import { BiMath } from "react-icons/bi";
import { MdChangeHistory } from "react-icons/md";
import { SiThemoviedatabase } from "react-icons/si";
import { FaCode } from "react-icons/fa";

const Category = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const Categories = [
    { name: "science", icon: MdOutlineScience },
    { name: "math", icon: BiMath },
    { name: "history", icon: MdChangeHistory },
    { name: "entertainment", icon: SiThemoviedatabase },
    { name: "programming", icon: FaCode },
  ];

  const handleComponent = (category) => {
    setSelectedCategory(category.name);
    setIsActive(true);
  };

  return (
    <>
      {!isActive ? (
        <VStack gap="5" minW="350px" maxW="100%">
          <Heading mb="50px">Choose Category</Heading>
          <Flex
            gap="5"
            justify="center"
            align="center"
            flexWrap="wrap"
            width="100%"
          >
            {Categories.map((item, index) => (
              <VStack
                key={index}
                onClick={() => handleComponent(item)}
                w="40%"
                gap="5px"
                p="10"
                bg="grey"
                borderRadius="10px"
              >
                <item.icon size="50px"/>
                <Text>{item.name.toUpperCase()}</Text>
              </VStack>
            ))}
          </Flex>
        </VStack>
      ) : (
        <Trivia prop={selectedCategory} /> // Render the Trivia component when isActive is false
      )}
    </>
  );
};

export default Category;
