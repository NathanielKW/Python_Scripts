import sys
import re
import os

def addNewLineToMessageExpression(string):
    occurrences = 0
    i = 0
    result = []

    while i < len(string):
        if string[i:i+2] == "++":
            occurrences += 1
            if occurrences % 2 == 0:
                result.append("\n")
            result.append("++")
            i += 2
        else:
            result.append(string[i])
            i += 1

    return ''.join(result)

def Main(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    for file in files:
        #read file lines into an array
        with open(directory + "/" + file, 'r') as f:
            lines = f.readlines()
        f.close()
            
        # create new array store all existing/modified lines into to write to file
        newLines = []

        # iterate over array and if we find a splunk logger line with a message attribute imbedded in the opening tag,
        # move message into new splunk logger message tag
        for line in lines:
            messageExpression = ""
            # finds splunk logger tags with message attribute
            if(re.search("^\s*<wuSplunkLogger:splunk-logger.+message=(\"|')", line)):
                
                # replace all '&quote' in line with double quote 
                strippedLine = re.sub("&quot;", '"', line)
                
                # replace instances of p() with Mule::p() in the stripped line
                strippedLine = re.sub("(?<!Mule::)(p\()(?=((\"|')\w+(\"|')\)))", "Mule::p(", strippedLine)
                
                # find message value expression in line and strip out all other characters
                
                # single quoted message attribute value case
                if(re.search("message='", strippedLine)):
                    messageExpression = re.sub("(^.*message=')|('.*/>$)", '', strippedLine)
                # double quoted message attribute value with mule expression
                elif (re.search("message=\"#\[", strippedLine)):
                    messageExpression = re.sub("(^.*message=\")|((?<=\])(\".*/>$))", '', strippedLine) 
                # double quoted message attribute value with no mule expression
                else:
                    messageExpression = re.sub("(^.*message=\")|(\".*/>$)", '', strippedLine)

                # for display purposes, add newline char before every even occurrence of "++" in the message expression
                messageExpression = addNewLineToMessageExpression(messageExpression)
                
                # strip out message and target attributes and their respective values from splunk logger tag
                strippedLine = re.sub("( message=(\"|')#\[.*\](\"|'))|( message='(\w| |\.)*')|( target=(\"|')\w*(\"|'))|(\/\B)", '', strippedLine)
                
                # find number of tabs or spaced tabs to append before our new xml tags
                numTabs = len(re.findall("(^\t)|(\t)\B", line))
                numSpacedTabs = len(re.findall("(^    )|(    )\B", line))
                tabPrefix = ""
                
                for i in range(numTabs + numSpacedTabs):
                    tabPrefix += "\t"

                # append line back into array without message attribute and value
                newLines.append(strippedLine)

                # add new message tag with captured message expression and add closing splunk logger tag
                newLine = tabPrefix + "\t<wuSplunkLogger:message ><![CDATA[" + messageExpression.strip() + "]]></wuSplunkLogger:message>\n"
                endTag = tabPrefix + "</wuSplunkLogger:splunk-logger>\n"
                newLines.append(newLine)
                newLines.append(endTag)

            # base case, no splunk logger tag with message attribute found. append whole line into new lines array
            # and replace instances of p("property") with Mule::p("property")
            else:
                newLine = re.sub("(?<!Mule::)(p\()(?=((\"|')\w+(\"|')\)))", "Mule::p(", line)
                #newLine = re.sub("&quot;", '"', newLine)
                newLines.append(newLine)

        # write whole array of lines to file
        with open(directory + "/" + file, 'w') as f:
            f.writelines(newLines)
        f.close()
    
    print("\nFinished Refactoring XML\n")

######################
# Main functionality #
######################

argLen = len(sys.argv)

if argLen == 1:
    directory = input("\nPlease enter the path to the desired /src/main/mule directory to refactor: ")
    Main(directory)

elif argLen == 2:
    directory = sys.argv[1]
    Main(directory)

else:
    print("To many parameters provided.\nPlease run script as follows:\n'Python ExampleFile.xml")