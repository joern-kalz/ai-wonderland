'use client'

import { useState } from "react";
import Menu from "./menu/Menu";
import Main from "./main/Main";

export default function Game() {
    const [sessionToken, setSessionToken] = useState<string>();

    function onStart() {
        setSessionToken('true');
    }

    if (sessionToken) {
        return <Main sessionToken={sessionToken} />;
    } else {
        return <Menu onStart={onStart} />;
    }

}