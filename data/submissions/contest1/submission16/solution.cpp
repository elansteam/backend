import {FC, useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {
    Avatar,
    Box, Button,
    Stack,
    SxProps,
    ToggleButton,
    ToggleButtonGroup,
    Typography,
    useTheme
} from "@mui/material";
import {getCurrentUser, getWithToken, UserType} from "../../api/auth.tsx";
import {ContestType, getContestById, getContestProblemsResources, sendSolution} from "../../api/api.tsx";
import CheckIcon from "@mui/icons-material/Check";
import ListAltIcon from '@mui/icons-material/ListAlt';
import MenuIcon from '@mui/icons-material/Menu';
import { Editor } from "@monaco-editor/react";
import { ThemeModeContext } from "../../Theme/index.ts";
import { useContext } from "react";
import Latex from "react-latex-next";


const ResultContent: FC = () => {
    return <div>

    </div>
}


type TaskResources = {
    name: string,
    legend: string,
    input: string, 
    output: string,
    scoring: string,
    notes: string,
    id: number
}

type TasksProps = {
    contest_id: any
}

const TasksContent: FC<TasksProps> = (props: TasksProps) => {

    const [tasksResources, setTasksResources] = useState<TaskResources[]>([]);
    const [taskText, setTaskText] = useState("test")
    const theme = useTheme();
    const { toggleTheme, themeMode, setThemeMode } = useContext(ThemeModeContext);

    const [currentState, setCurrentState] = useState(0);

    const [statesNum, setStatesNum] = useState(0);

    const [navButtons, setNavButtons] = useState<any>([]);

    const [code, setCode] = useState<string[]>(["// your code here!"])

    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    const [editorState, setEditorState] = useState<"show" | "hide">("show")


    useEffect(() => {
        async function setup() {
            const contestProblemsResources = await getContestProblemsResources(props.contest_id)
            

            setStatesNum(contestProblemsResources.length)
            let toChange = []
            for (let i = 0; i < contestProblemsResources.length; ++i) {
                toChange.push(
                    <Button key={i} value={i} variant={currentState == i ? "filled" : "outlined"} color="secondary" onClick={handleChangeState}>{alphabet[i]}</Button>
                )
            }
            setNavButtons(toChange);
            setTasksResources(contestProblemsResources);

            let current_code = code;
            while (current_code.length > contestProblemsResources.length) {
                current_code.pop();
            }

            while (current_code.length < contestProblemsResources.length) {
                current_code.push("// your code here!");
            }

            setCode(current_code);
        }

        setup();

    }, [currentState]);


    const rootStyles: SxProps = {
        padding: "40px",
        height: "100%",
        marginBottom: "40px"
    }

    const navStyles: SxProps = {
        display: "flex",
        marginBottom: "30px",
        overflow: "scroll",
        justifyContent: "space-between"
    }

    const taskStyles: SxProps = {
        backgroundColor: `${theme.palette.surfaceContainerHigh.main}`,
        borderRadius: "30px",
        overflow: "scroll",
        padding: "20px",
        height: "100%",
        paddingBottom: "150px",
        display: "flex"
    }


    const handleChangeState = (e: any) => {
        setCurrentState(e.target.value)
    }


    const handleSubmit = async () => {
        const response = await sendSolution(props.contest_id, tasksResources[currentState].id, code[currentState]);

        if (response === undefined) {
            alert("Error occured")
        } else  {
            console.log(props.contest_id, tasksResources[currentState].id);
        }
    }

    // katex.render("c = \\pm\\sqrt{a^2 + b^2}", element, {
    //     throwOnError: false
    // });

    const handleEditorState = () => {
        if (editorState == "show") {
            setEditorState("hide")
        } else {
            setEditorState("show")
        }
    }

    return <Box sx={rootStyles}>
        <Box sx={navStyles}>
            <Stack spacing={2} direction="row">
                {navButtons}
            </Stack>
            <Stack spacing={2} direction="row">
                <Button variant={editorState == "show" ? "filled" : "outlined"} color="secondary" onClick={handleEditorState}>Editor</Button>
            </Stack>
        </Box>
        <Box sx={taskStyles}>
            <Box>
                <Box sx={{
                    marginBottom: "20px"
                }}>
                    <Typography variant="h3" fontWeight="bold" mb="20px">
                        {alphabet[currentState]}. {tasksResources[currentState]?.name}
                    </Typography>
                    <Typography variant="h5" mb="20px">
                        <Latex>
                            {tasksResources[currentState]?.legend|| ""}
                        </Latex>
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                        Формат входных данных
                    </Typography>
                    <Typography variant="h5" mb="20px">
                        <Latex>
                            {tasksResources[currentState]?.input || ""}
                        </Latex>
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                        Формат выходных данных
                    </Typography>
                    <Typography variant="h5"  mb="20px">
                        <Latex>
                            {tasksResources[currentState]?.output || ""}
                        </Latex>
                    </Typography>
                    <Typography variant="h4" fontWeight="bold">
                        Примечание
                    </Typography>
                    <Typography variant="h5" mb="20px">
                        <Latex>
                            {tasksResources[currentState]?.notes || ""}
                        </Latex>
                    </Typography>
                </Box>
            </Box>
            <Box sx={{
                display: "flex",
                flexDirection: "column",
                marginLeft: "30px"
            }}>
                <Box sx={{
                    borderRadius: "30px",
                    height: "700px",
                    overflow: "hidden",
                    minWidth: "800px",
                    display: `${editorState == "show" ? "block" : "none"}`
                }}>
                    <Editor
                        options={{
                            fontSize: 20,
                            formatOnType: true,
                        }}
                        theme={themeMode == "light" ? "" : "vs-dark" }
                        height="100%"
                        width="100%"
                        language="cpp"
                        value={code[currentState]}
                        onChange={(code_new: any) => {
                            let current_code = code;
                            current_code[currentState] = code_new;
                            setCode(current_code);
                        }}
                        />

                </Box>
                <Typography variant="h2" sx={{
                    alignSelf: "flex-end"
                }}>
                    <Button variant="filled" onClick={handleSubmit} sx={{
                    display: `${editorState == "show" ? "inline" : "none"}`
                    }}>Send solution!</Button>
                </Typography>
            </Box>
        </Box>
    </Box>
}

const Contest: FC = () => {

    const [_user, setUser] = useState<UserType | undefined>();
    const [contest, setContest] = useState<ContestType | undefined>(undefined);

    // const navigate = useNavigate();

    const theme = useTheme();

    const {id} = useParams();


    useEffect(() => {
        async function temp() {
            setUser(await getCurrentUser());
            // @ts-ignore
            setContest(await getContestById(parseInt(id)));
        }

        temp();
    }, []);

    const rootStyles: SxProps = {
        borderRadius: "30px",
        backgroundColor: `${theme.palette.surfaceContainerLow.main};`,
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        position: "fixed",
        // paddingBottom: "100px"
    }

    const userStyles: SxProps = {
        paddingTop: "80px",
        display: "none",
        flexDirection: "column",
        alignItems: "center",
        color: `${theme.palette.onSurface.main}`,
        minWidth: "350px",
        marginLeft: "30px"
    }

    const navStyles: SxProps = {
        width: "100%",
        paddingLeft: "60px",
        paddingRight: "300px",
        flexGrow: "grow",
        flexDirection: "column",
        justifyContent: "center",
        display: "flex",
        position: "static"
    }

    const avatarStyles = {
        width: "300px",
        height: "300px",
        marginBottom: "10px"
    }

    const navButtonsStyles: SxProps = {
        width: "100%",
        paddingBottom: "20px",
        paddingTop: "20px"
    }

    const dataStyles: SxProps = {
        backgroundColor: `${theme.palette.surfaceContainerLowest.main}`,
        borderRadius: "30px",
        height: "100vh",
        paddingBottom: "100px"
    }

    const [alignment, setAlignment] = useState<string>("tasks");

    const [content, setContent] = useState<any>(<TasksContent contest_id={id}/>);
    //
    const handleAlignment = (_event: React.MouseEvent<HTMLElement>,
                             newAlignment: string) => {
        if (newAlignment != null) {
            setAlignment(newAlignment);
            if (newAlignment == "tasks") {
                setContent(<TasksContent contest_id={id}/>);
            } else if (newAlignment == "result") {
                setContent(<ResultContent/>);
            }
        }
    };

    const nameStyles: SxProps = {
        width: "300px",
        whiteSpace: "pre-line",
        wordWrap: "break-word",
        overflow: "wrap"
    }

    return <>
        <Box sx={rootStyles}>
            <Box sx={userStyles}>
                <Avatar sx={avatarStyles}>
                    <Typography fontSize="400%">
                        {contest?.name[0]}{contest?.name[1]}
                    </Typography>
                </Avatar>
                <Box sx={nameStyles}>
                    <Typography fontWeight="bold" variant="h4" sx={{color: `${theme.palette.onSurface.main}`, textAlign:"left"}}>
                        {contest?.name}
                    </Typography>
                </Box>
                <Box sx={nameStyles}>
                    <Typography variant="body1">
                        {contest?.description}
                    </Typography>
                </Box>
            </Box>
            <Box sx={navStyles}>
                <Box sx={navButtonsStyles}>
                    <Stack direction="row" spacing={2}>
                        <ToggleButtonGroup fullWidth={true} exclusive value={alignment} onChange={handleAlignment}>
                            <ToggleButton fullWidth={true} value="tasks">
                                {alignment === 'tasks' ? <CheckIcon sx={{mr: 1}}/> : <MenuIcon sx={{mr: 1}}/>}
                                Tasks
                            </ToggleButton>
                            <ToggleButton fullWidth={true} value="result">
                                {alignment === "result" ? <CheckIcon sx={{mr: 1}}/> : <ListAltIcon sx={{mr: 1}}/>}
                                Result
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </Stack>
                </Box>
                <Box sx={dataStyles}>
                    {content}
                    {/* <TasksContent/> */}
                </Box>
            </Box>
        </Box>
    </>
}


export default Contest